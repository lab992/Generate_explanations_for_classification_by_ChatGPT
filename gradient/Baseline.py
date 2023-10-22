import tkinter as tk
from tkinter import filedialog
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.dummy import DummyClassifier
# from sklearn.impute import KNNImputer


def split(dataset):
    X = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    # knn_imputer = KNNImputer(n_neighbors=3)
    # X_imputed = knn_imputer.fit_transform(X)
    X_imputed = X.fillna(0.0)
    return X_imputed , y

def rf():
    # 加载数据集（以鸢尾花数据集为例）
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    file_1 = filedialog.askopenfilename()
    train = pd.read_table(file_1, sep = '\s+', header=None)
    file_2 = filedialog.askopenfilename()
    test = pd.read_table(file_2, sep = '\s+', header=None)
    
    X_train, y_train = split(train.iloc[list(range(30,60)) + list(range(60,90))])

    # test ABCD 各10个
    X_test, y_test = split(test.iloc[list(range(70,140)) + list(range(140,210))])

    # 创建XGBoost分类器
    # model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss')

    # 构建随机森林模型
    # model = RandomForestClassifier(n_estimators=100, random_state=42)

    # 决策树
    model = DecisionTreeClassifier(random_state=42)

    # Dummy classifier
    # model = DummyClassifier(strategy='stratified', random_state = 42)

    le = LabelEncoder()
    y_train = le.fit_transform(y_train)
    y_test = le.fit_transform(y_test)
    # 训练模型
    model.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = model.predict(X_test)

    # 计算准确度
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')


if __name__ == "__main__":
    rf()