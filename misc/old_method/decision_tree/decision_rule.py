import numpy as np
from sklearn.tree import _tree
import re
import pandas as pd



def translation_to_rules(translations):

    sentences = []
    sorted_translations = sorted(translations, key=len)

    for translation in sorted_translations:

        sentence = "If there's "
        class_name = translation[0]
        rest_array = translation[1:]

        if len(rest_array) == 1:
            sentence += rest_array[0]
        else:
            for i in range(len(rest_array)):
                if len(rest_array) != 1:
                    sentence += "and " + rest_array[i]
                else:
                    sentence += rest_array[i] + ", "

        sentence += ", then '" + class_name + "'."
        sentences.append(sentence)
    
    result_rules = "\n".join(sentences)
    return result_rules



def transfer_conditions(conditions):

    lookup_table = pd.read_csv('selected_dataset/lookup_table.csv', sep = ',')

    pattern = re.compile(r'(\S+)\s*([<>]=?)\s*([-+]?\d*\.?\d+|\.\d+)')

    result = []

    temp_lookup_table = pd.DataFrame(columns=['feature', 'meaning', 'type', 'tf', 'value'])

    for condition in conditions:

        classification = condition[0]
        situations = condition[1:]
        temp_result = []
        temp_result.append(classification)

        for situation in situations:

            match = pattern.match(situation)

            feature_name = ""
            operator = ""
            value = ""

            if match:
                feature_name += match.group(1)
                operator += match.group(2)
                value += match.group(3)
            else:
                raise ValueError("Not match.")

            feature_list = lookup_table['feature']
            row_index = -1
            for i in range(len(feature_list)):
                if feature_list.iloc[i] in feature_name:
                    row_index += i + 1
                    break
            
            if row_index == -1:
                raise ValueError("Not in lookup table.")

            filtered_rows = lookup_table.iloc[row_index]
            meaning = filtered_rows['meaning']
            type = filtered_rows['type']
            tf = filtered_rows['tf']

            describe = []
            if type == "adj":
                describe.append("a slight ")
                describe.append("a big ")
            elif type == "n":
                describe.append("few ")
                describe.append("a lot of ")

            translation = ""

            if operator == "<=":
                if tf == 0:
                    translation += describe[0] + meaning
                elif tf == 1:
                    translation += describe[1] + meaning
                else:
                    raise ValueError("tf should be 0 or 1.")
            else:
                if tf == 0:
                    translation += describe[1] + meaning
                elif tf == 1:
                    translation += describe[0] + meaning
                else:
                    raise ValueError("tf should be 0 or 1.")
            
            if not any(temp_lookup_table['feature'] == filtered_rows['feature']):
                temp_lookup_table = temp_lookup_table.loc[len(temp_lookup_table)]({'feature': filtered_rows['feature'], 
                                                            'meaning': meaning, 
                                                            'type': type, 
                                                            'tf': tf, 
                                                            'value': value}, 
                                                            ignore_index=True)
            
            temp_result.append(translation)
        
        result.append(temp_result)

    return result, temp_lookup_table
        


    


def to_conditions(merged_rules):
    
    conditions = []
    for i in range(len(merged_rules)):
        condition = []
        class_index = merged_rules[i].find("class: ") + len("class: ")
        class_word = merged_rules[i][class_index:].split()[0]
        condition.append(class_word)
        matches = re.findall(r'\((.*?)\)', merged_rules[i])
        condition.extend(matches)
        conditions.append(condition)
    
    return conditions

# Function to merge nodes with the same class
def merge_nodes(tree, node_id=0):
    # If not a leaf node
    if tree.children_left[node_id] != tree.children_right[node_id]:  
        merge_nodes(tree, tree.children_left[node_id])
        merge_nodes(tree, tree.children_right[node_id])

        # Check if both children have the same class
        if tree.value[tree.children_left[node_id]].argmax() == tree.value[tree.children_right[node_id]].argmax():
            # Merge the children by updating the values in the parent node
            tree.value[node_id] = tree.value[tree.children_left[node_id]] + tree.value[tree.children_right[node_id]]
            # Make the left child point to the right child
            tree.children_left[node_id] = tree.children_right[node_id]

def get_rules(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []
    
    def recurse(node, path, paths):
        
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]
            
    recurse(0, path, paths)

    # sort by samples count
    samples_count = [p[-1][1] for p in paths]
    ii = list(np.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]
    
    rules = []
    for path in paths:
        rule = "if "
        
        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += str(p)
        rule += " then "
        if class_names is None:
            rule += "response: "+str(np.round(path[-1][0][0][0],3))
        else:
            classes = path[-1][0][0]
            l = np.argmax(classes)
        #     rule += f"class: {class_names[l]} (proba: {np.round(100.0*classes[l]/np.sum(classes),2)}%)"
        # rule += f" | based on {path[-1][1]:,} samples"
            rule += "\n"
            rule += f"class: {class_names[l]}"
        rules += [rule]
        
    return rules

def merge_rules(rules):
    for i in range(len(rules)):
        fst = rules[i].split('and')
        for j in range(i + 1, len(rules)):
            snd = rules[j].split('and')
            fst_then_class = fst[-1][-14:]
            snd_then_class = snd[-1][-14:]
            if len(fst) == len(snd) and fst[:-1] == snd[:-1] and fst_then_class == snd_then_class and compare_strings(fst[-1], snd[-1]):
                and_string = 'and'.join(fst[:-1])
                final_result = and_string + fst_then_class
                rules[i] = final_result
                rules[j] = final_result
    return list(set(rules))
                        
def compare_strings(str1, str2):
    if abs(len(str1) - len(str2)) == 1:
        return True
    else:
        return False
