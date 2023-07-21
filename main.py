from util import IO, PromptGenerator, GPTExcecutor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from tsfresh.transformers import RelevantFeatureAugmenter
import pandas as pd


def pipeline():

    X_train, X_test, y_train, y_test = IO.read_file()

    # define pipeline
    pipeline = Pipeline([
        # ('imputer', SimpleImputer()),  # 填补缺失值
        # ('scaler', StandardScaler()),  # 标准化
        ('augmenter', RelevantFeatureAugmenter())
        ('prompt', PromptGenerator(X_train, X_test, y_train))
        ('GPT', GPTExcecutor())
    ])

    pipeline.fit(X_train, y_train)

if __name__ == "__main__":
    pipeline()