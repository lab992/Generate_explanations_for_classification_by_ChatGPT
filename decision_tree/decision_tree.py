import tkinter as tk
from tkinter import filedialog
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier, export_graphviz, plot_tree, export_text
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from decision_rule import get_rules,merge_nodes, merge_rules

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
    X_test = pd.read_csv(file_2).iloc[:, 1:]

    target_values = [2, 3, 4]
    repeat_counts_train = [30, 30, 30]
    repeat_counts_test = [70, 70, 70]

    # 使用 Pandas 创建 Series
    y_train = pd.Series([val for val, count in zip(target_values, repeat_counts_train) for _ in range(count)], name='target')
    y_test = pd.Series([val for val, count in zip(target_values, repeat_counts_test) for _ in range(count)], name='target')
    
    # X_train, y_train = split(train.iloc[list(range(30, 120))])

    # # test ABCD 各10个
    # X_test, y_test = split(test.iloc[list(range(70, 280))])

    X_train = X_train.iloc[:, 0: 5]
    X_test = X_test.iloc[:, 0: 5]

    model = DecisionTreeClassifier(random_state=42, min_samples_leaf=6)

    le = LabelEncoder()
    y_train = le.fit_transform(y_train)
    y_test = le.fit_transform(y_test)
    # 训练模型
    clf = model.fit(X_train, y_train)

    # Apply the merge function
    merge_nodes(clf.tree_)

    # # 在测试集上进行预测
    # y_pred = model.predict(X_test)
    # # 计算准确度
    # accuracy = accuracy_score(y_test, y_pred)
    # print(f'Accuracy: {accuracy}')

    # with open("tsfresh_feature.txt", 'w') as f:
    #     f.write(export_text(clf))

    rules = get_rules(clf, X_train.columns.to_numpy(), ["2","3","4"])
    
    merged_rules = merge_rules(rules)
    
    for i in range(len(merged_rules)):
        with open("f_5_min_6_full_merged.txt", 'a') as f:
            f.write(merged_rules[i])
            f.write('\n')


    # fig = plt.figure(figsize=(50, 40))
    # _ = plot_tree(
    #     clf,
    #     feature_names = X_train.columns.to_list(),
    #     class_names = ["2","3","4"],
    #     filled = True
    # )

    # fig.savefig("decision_tree_f_5_min_6_MERGED2.png")


def feature_ex():
    # # 加载数据集（以鸢尾花数据集为例）
    # root = tk.Tk()
    # root.withdraw()

    # # Open file selection window
    # files = filedialog.askopenfilename()
    # data = pd.read_csv(files)
    # two_to_four = data.iloc[list(range(30, 120))]
    # y = two_to_four['target']
    # X = two_to_four.drop('target', axis=1).iloc[:, 1:]
    # feature_names = X.columns

    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # 决策树
    model = DecisionTreeClassifier(random_state=42)

    clf = model.fit(X, y)

    feature_names = iris.feature_names,
    class_names = iris.target_names,


    fig = plt.figure(figsize=(25, 20))
    _ = plot_tree(
        clf,
        feature_names = iris.feature_names,
        class_names = iris.target_names,
        filled = True
    )

    fig.savefig("decision_tree.png")

    # # 获取特征重要性得分
    # feature_importance = model.feature_importances_

    # # 创建特征索引、名称和重要性得分的元组列表
    # feature_info_list = [(index, name, score) for index, name, score in zip(range(len(feature_names)), feature_names, feature_importance)]

    # # 根据重要性得分降序排列
    # feature_info_list.sort(key=lambda x: x[2], reverse=True)

    # # 获取前20个最重要的特征信息
    # top_feature_info = feature_info_list[:20]

    # # 打印最重要的20个特征的信息
    # for index, name, score in top_feature_info:
    #     print(f"{name}, Importance Score = {score:.4f}")

    # with open("tsfresh_test.dot", 'w') as f:
    #     f = export_graphviz(clf, out_file=f)
        
if __name__ == "__main__":
    accuracy()
    # feature_ex()