from tsfresh import select_features, extract_relevant_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import select_features,extract_features

def cal_features(X, y):

    extracted_features = extract_features(X, column_id="id", column_sort="Time (s)")
    # extracted_features = extract_features(X, column_id="id", column_sort="time")

    # extracted_features.to_csv('HMP_extracted.csv')

    impute(extracted_features)

    features_filtered = select_features(extracted_features, y)

    features_filtered.to_csv('BASKET_filtered.csv')
