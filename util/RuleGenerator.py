import numpy as np
from sklearn.tree import DecisionTreeClassifier, _tree
import re
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# The general pipeline of extraction rules from decision tree
# transfrom desicion tree to the class description in context
# lookup table is to help transfer test samples
def gen_rules(X_train, y_train):

    model = DecisionTreeClassifier(random_state=42, min_samples_leaf=7)

    class_names = y_train.unique()
    
    le = LabelEncoder()
    y_train = le.fit_transform(y_train)

    clf = model.fit(X_train, y_train)

    # Apply the merge function
    merge_nodes(clf.tree_)

    # get rough classification rules
    rules = get_rules(clf, X_train.columns.to_numpy(), class_names)
    
    merged_rules = merge_rules(rules)

    conditions = to_conditions(merged_rules)

    translations, temp_lookup_table = transfer_conditions(conditions)

    return translations, temp_lookup_table

# Assemble description of classification rules to a complete text.
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
                if i == len(rest_array) - 1:
                    sentence += "and " + rest_array[i]
                else:
                    sentence += rest_array[i] + ", "

        sentence += ", then '" + class_name + "'."
        sentences.append(sentence)
    
    result_rules = "\n".join(sentences)
    return result_rules

# Transfer conditions to a description of classification rules.
# This process create a lookup table which help transform test samples later.
def transfer_conditions(conditions):

    lookup_table = pd.read_csv('selected_dataset/lookup_table.csv', sep = ',')

    # find feature like 'agg_linear_trend__attr_"intercept"__chunk_len_5__f_agg_"min"'
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
                new_row = pd.Series({'feature': filtered_rows['feature'], 
                                    'meaning': meaning, 
                                    'type': type, 
                                    'tf': tf, 
                                    'value': value})
                temp_lookup_table = pd.concat([temp_lookup_table, pd.DataFrame([new_row])], ignore_index=True)
            
            temp_result.append(translation)
        
        result.append(temp_result)
        
    return result, temp_lookup_table
        
# break down classification rules to conditions
# e.g. if (acceleration__number_crossing_m__m_1 <= 4.5) and (acceleration__agg_linear_trend__attr_"intercept"__chunk_len_5__f_agg_"min" > -0.438) then class: 3
# To ['3', 'acceleration__number_crossing_m__m_1 <= 4.5', 'acceleration__agg_linear_trend__attr_"intercept"__chunk_len_5__f_agg_"min" > -0.438']
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

# Extract classification rules from decision tree
def get_rules(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []
    
    # record each path
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
    
    # transform to sentence
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

# merge rules
# merged rules should satisfy both 3 situations:
# 1) 2 rules have the same class
# 2) conditions beside the last condition should be the same
# 3) the last condition of 2 rules should be like: 1. feature_1 <= 3, 2. feature_1 > 3

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
                        
# compare whether the difference of length of 2 string equals 1
# this to compare whether 2 condition are describing same feature but one is '<=' and the other one is '>'
def compare_strings(str1, str2):
    if abs(len(str1) - len(str2)) == 1:
        return True
    else:
        return False
