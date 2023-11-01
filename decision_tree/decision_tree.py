import tkinter as tk
from tkinter import filedialog
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier, export_graphviz, plot_tree, export_text
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from decision_rule import get_rules,merge_nodes, merge_rules
from feature_to_prompt import feature_to_prompt, gen_context, array_to_query, each_feature_description_context, class_description_context
from GPTExecutor import gpt_execution

def split(dataset):
    X = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    X_imputed = X.fillna(0.0)
    return X_imputed , y

def accuracy():
    root = tk.Tk()
    root.withdraw()

    file_1 = filedialog.askopenfilename()
    X_train = pd.read_csv(file_1).iloc[:, 1:]
    file_2 = filedialog.askopenfilename()
    X_test = pd.read_csv(file_2).iloc[:, 1:].iloc[list(range(0,20)) + list(range(70,90)) + list(range(140,160))]

    target_values = [2, 3, 4]
    repeat_counts_train = [30, 30, 30]
    repeat_counts_test = [20, 20, 20]

    # 使用 Pandas 创建 Series
    y_train = pd.Series([val for val, count in zip(target_values, repeat_counts_train) for _ in range(count)], name='target')
    y_test = pd.Series([val for val, count in zip(target_values, repeat_counts_test) for _ in range(count)], name='target')
    
    # X_train, y_train = split(train.iloc[list(range(30, 120))])

    # # test ABCD 各10个
    # X_test, y_test = split(test.iloc[list(range(70, 280))])

    X_train = X_train.iloc[:, 0: 3]
    X_test = X_test.iloc[:, 0: 3]

    model = DecisionTreeClassifier(random_state=42, min_samples_leaf=7)

    le = LabelEncoder()
    y_train = le.fit_transform(y_train)
    y_test = le.fit_transform(y_test)
    # 训练模型
    clf = model.fit(X_train, y_train)

    # Apply the merge function
    merge_nodes(clf.tree_)

    # # 在测试集上进行预测
    # y_pred = model.predict(X_test)
    # print(y_pred)
    # # 计算准确度
    # accuracy = accuracy_score(y_test, y_pred)
    # print(f'Accuracy: {accuracy}')

    # rules = get_rules(clf, X_train.columns.to_numpy(), ["2","3","4"])
    
    # merged_rules = merge_rules(rules)
    
    test_sets = feature_to_prompt(X_test).to_numpy()
    # # test_test_sets = array_to_query(test_sets)

    # context = '\n'.join(merged_rules) + each_feature_description_context()
  
    # gpt_execution(context, X_test.to_numpy())



    context = gen_context()


    gpt_execution(context, test_sets)

    
    # with open("prompt_test_0.txt", "a") as file:
    #     file.write(context + test_test_sets[0])


    # for i in range(len(merged_rules)):
    #     with open("f_5_min_7_full_merged.txt", 'a') as f:
    #         f.write(merged_rules[i])
    #         f.write('\n') 


    # fig = plt.figure(figsize=(50, 40))
    # _ = plot_tree(
    #     clf,
    #     feature_names = X_train.columns.to_list(),
    #     class_names = ["2","3","4"],
    #     filled = True
    # )

    # fig.savefig("decision_tree_f_5_min_8_MERGED.png")

def to_gpt_method():
    root = tk.Tk()
    root.withdraw()

    file_txt = filedialog.askopenfilename()

    with open(file_txt, 'r') as file:
        content = file.read()

    sentences_array = content.split('\n')

    # Remove any empty strings from the array
    sentences_array = [sentence for sentence in sentences_array if sentence]

    context = class_description_context()

    gpt_execution(context, sentences_array)

if __name__ == "__main__":
    accuracy()
    # to_gpt_method()