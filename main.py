from util import IO, PromptGenerator, GPTExecutor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
# from tsfresh.transformers import RelevantFeatureAugmenter
# from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import impute

import matplotlib.pyplot as plt

import pandas as pd


def pipeline():

    X_train, X_test, y_train, y_test = IO.read_file()

    # define pipeline
    # pipeline = Pipeline([
    #     ('imputer', SimpleImputer()),  # 填补缺失值
    #     ('scaler', StandardScaler()),  # 标准化
    #     ('selector', SelectKBest(k=10))
    #     # ('prompt', PromptGenerator(X_train, X_test, y_train))
    #     # ('GPT', GPTExecutor())
    # ])

    # pipeline.fit(X_train, y_train)

    # # 创建SelectKBest对象并进行特征选择
    # k_best = SelectKBest(k=10)
    # X_new = k_best.fit_transform(impute(X_train), y_train)

    # # 获取被选中的特征的索引
    # selected_feature_indices = k_best.get_support(indices=True)

    # print(selected_feature_indices)


if __name__ == "__main__":
    pipeline()