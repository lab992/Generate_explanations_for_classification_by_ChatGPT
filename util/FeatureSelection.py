from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import select_features,extract_features
from sklearn.tree import DecisionTreeClassifier

# The general process of feature selection
def feature_selection(X_train, X_test, y_train, feature_amount):
    # extract filtered features of train samples
    extracted_train = cal_extracted_features(X_train)
    filtered_train = cal_filtered_features(extracted_train, y_train)

    # extract features of test samples (not filtered)
    extracted_test = cal_extracted_features(X_test)

    # generate names of important features
    selected_feature = extract_important_features(filtered_train, y_train, feature_amount)

    # select only important features
    train_set = extracted_train[selected_feature]
    test_set = extracted_test[selected_feature]

    # removes the prefix in the column names
    # tsfresh used to set column name of value as a prefix before each feature
    train_set.columns = train_set.columns.str.replace(r'^.*?__', '')
    test_set.columns = test_set.columns.str.replace(r'^.*?__', '')
    return train_set, test_set

# For both train samples and test samples, extract features by TSFRESH
def cal_extracted_features(X):

    extracted_features = extract_features(X, column_id="id", column_sort="time")
    impute(extracted_features)

    return extracted_features

# Only for train samples, filter features
def cal_filtered_features(extracted_features, y):

    filtered_features = select_features(extracted_features, y)

    return filtered_features

# use decision tree to rank features according to importance
# select top X features, X = feature_amount
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





