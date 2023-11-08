import tkinter as tk
from tkinter import filedialog
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from matplotlib import pyplot as plt


def origin():
    # 加载数据集（以鸢尾花数据集为例）
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    file_1 = filedialog.askopenfilename()
    train = pd.read_table(file_1, sep = '\s+', header=None)
    file_2 = filedialog.askopenfilename()
    test = pd.read_table(file_2, sep = '\s+', header=None)
    
    X_train, y_train = split(train.iloc[list(range(30,60)) + list(range(60,90)) + list(range(90,120))])

    # test ABCD 各10个
    X_test, y_test = split(test.iloc[list(range(70,90)) + list(range(140,160)) + list(range(210,230))])

    return X_train, X_test, y_train, y_test

def feature_type():
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

    X_train = X_train.iloc[:, 0: 3]
    X_test = X_test.iloc[:, 0: 3]

    return X_train, X_test, y_train, y_test
    


def split(dataset):
    X = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    # knn_imputer = KNNImputer(n_neighbors=3)
    # X_imputed = knn_imputer.fit_transform(X)
    X_imputed = X.fillna(0.0)
    return X_imputed , y

def rf():

    X_train, X_test, y_train, y_test = feature_type()

    # 决策树
    model = DecisionTreeClassifier(random_state=42, min_samples_leaf = 7)

    le = LabelEncoder()
    y_train = le.fit_transform(y_train)
    y_test = le.fit_transform(y_test)
    # 训练模型
    clf = model.fit(X_train, y_train)

    # 在测试集上进行 预测
    y_pred = model.predict(X_test)

    # 计算准确度
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

    print(y_pred)

    # fig = plt.figure(figsize=(25, 20))
    # _ = plot_tree(
    #     clf,
    #     feature_names = ["feature_1", "feature_2","feature_3"],
    #     class_names = ["2","3","4"],
    #     filled = True
    # )

    # fig.savefig("decision_tree_f_3_min_7.png")


if __name__ == "__main__":
    rf()