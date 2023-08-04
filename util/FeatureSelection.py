from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import select_features,extract_features

def cal_features(X, y):

    extracted_features = extract_features(X, column_id="id", column_sort="time")

    impute(extracted_features)
    features_filtered = select_features(extracted_features, y)

    features_filtered.to_csv('filtered.csv')