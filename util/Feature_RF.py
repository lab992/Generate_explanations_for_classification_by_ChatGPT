import tkinter as tk
from tkinter import filedialog
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

def rf():
    # 加载数据集（以鸢尾花数据集为例）
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilename()
    data = pd.read_csv(files)
    y = data['target']
    X = data.drop('target', axis=1).iloc[:, 1:]
    feature_names = X.columns

    # 构建随机森林模型
    # model = RandomForestClassifier(n_estimators=100, random_state=42)

    # 梯度提升树
    # model = xgb.XGBRegressor()

    # 决策树
    model = DecisionTreeClassifier(random_state=42)

    model.fit(X, y)

    # 获取特征重要性得分
    feature_importance = model.feature_importances_

    # 创建特征索引、名称和重要性得分的元组列表
    feature_info_list = [(index, name, score) for index, name, score in zip(range(len(feature_names)), feature_names, feature_importance)]

    # 根据重要性得分降序排列
    feature_info_list.sort(key=lambda x: x[2], reverse=True)

    # 获取前20个最重要的特征信息
    top_feature_info = feature_info_list[:20]

    # 打印最重要的20个特征的信息
    for index, name, score in top_feature_info:
        print(f"{name}, Importance Score = {score:.4f}")

    # 选取前20个最重要的特征
    # selected_features = X[:, top_feature_indices]

    # 在这里你可以使用selected_features继续进行建模等操作

if __name__ == "__main__":
    rf() 