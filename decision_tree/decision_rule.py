import numpy as np
from sklearn.tree import _tree

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

def dictionary():
    level_2 = ["low", "high"]
    level_3 = ["low", "medium", "high"]
    level_4 = ["very low", "low", "high", "very high"]
    level_5 = ["very low", "low", "medium", "high", "very high"]
