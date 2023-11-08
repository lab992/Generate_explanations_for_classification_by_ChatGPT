import numpy as np
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import select_features,extract_features
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from matplotlib import pyplot as plt

def feature_selection(X_train, X_test, y_train, feature_amount):
    extracted_train = cal_extracted_features(X_train)
    
    filtered_train = cal_filtered_features(extracted_train, y_train)
    extracted_test = cal_extracted_features(X_test)
    selected_feature = extract_important_features(filtered_train, y_train, feature_amount)

    train_set = extracted_train[selected_feature]
    test_set = extracted_test[selected_feature]

    train_set.columns = train_set.columns.str.replace(r'^.*?__', '')
    test_set.columns = test_set.columns.str.replace(r'^.*?__', '')
    return train_set, test_set

def cal_extracted_features(X):

    extracted_features = extract_features(X, column_id="id", column_sort="time")
    impute(extracted_features)

    return extracted_features

def cal_filtered_features(extracted_features, y):

    filtered_features = select_features(extracted_features, y)

    return filtered_features


def extract_important_features(X, y, feature_amount):

    X = X.iloc[:, 1:]
    feature_names = X.columns

    model = DecisionTreeClassifier(random_state=42)
    clf = model.fit(X, y)

    # get importance of features
    feature_importance = model.feature_importances_
    feature_info_list = [(name, score) for name, score in zip(feature_names, feature_importance)]
    feature_info_list.sort(key=lambda x: x[1], reverse=True)
    top_feature_info = feature_info_list[:feature_amount]
    selected_features = [tup[0] for tup in top_feature_info]

    return selected_features





