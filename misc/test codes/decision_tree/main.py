# 导入所需的库
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def toCSV():
    # Create main window
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilenames()
    for file_path in files:
        # 打开文本文件进行读取
        with open(file_path, 'r') as file:
            text = file.read()

        # 将空格替换为逗号
        text = text.replace(' ', ',')

        # 将替换后的文本写入到新的文件
        with open(file_path[:-3] + 'csv', 'w') as file:
            file.write(text)


def run(X_train, X_test, y_train, y_test):

    # 创建决策树分类器
    clf = DecisionTreeClassifier()

    # 训练模型
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_test)
    print(y_pred)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    print("准确率：", accuracy)

    return y_pred 

if __name__ == "__main__":


    # 从CSV文件读取数据
    X_train = pd.read_csv("acutenephritis_Xlearn.csv")
    X_test = pd.read_csv("acutenephritis_Xtest.csv")
    y_train = pd.read_csv("acutenephritis_Ylearn.csv")
    y_test = pd.read_csv("acutenephritis_Ytest.csv")

    # X_train, X_test, y_train, y_test = dataset()
    for _ in range(15):
        y = run(X_train, X_test, y_train, y_test)
        with open('result2.txt', "a") as file:
            file.write(', '.join(map(str, y)))
            file.write("\n")
    # toCSV()