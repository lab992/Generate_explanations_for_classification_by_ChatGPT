from util import FileReader, PromptGenerator, GPTExecutor, FeatureSelection
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
# from tsfresh.transformers import RelevantFeatureAugmenter
# from tsfresh import extract_features, select_features

import matplotlib.pyplot as plt

import pandas as pd


def pipeline():

    # X_train, X_test, y_train, y_test = FileReader.read_file_acc()

    # X, y = FileReader.read_file_basket()

    # X, y = FileReader.read_file_HMP()
    
    # # define pipeline
    # pipeline = Pipeline([
    #     ('imputer', SimpleImputer()),  # 填补缺失值
    #     ('scaler', StandardScaler()),  # 标准化
    #     ('prompt', PromptGenerator(X_train, X_test, y_train))
    #     ('GPT', GPTExecutor())
    # ])

    context, query = PromptGenerator.prompt_gen()
    GPTExecutor.gpt_execution(context, query)

    # with open("prompt_RF.txt", "w") as f:
    #     f.writelines(context)
    #     f.writelines(query)

    # print("OK")

    # FeatureSelection.cal_features(X_train, y_train)

    # FeatureSelection.cal_features(X, y)

    # pipeline.fit(X_train, y_train)



if __name__ == "__main__":
    pipeline() 