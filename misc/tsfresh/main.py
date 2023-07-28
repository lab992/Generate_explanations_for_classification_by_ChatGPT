import pandas as pd
from tsfresh import extract_features, extract_relevant_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_selection import select_features
from tsfresh.feature_selection.relevance import calculate_relevance_table
from tsfresh.examples.robot_execution_failures import (
    download_robot_execution_failures,
    load_robot_execution_failures,
)
from tsfresh.feature_extraction import MinimalFCParameters

def my_extraction():
    # Download the dataset
    download_robot_execution_failures()

    # Load the dataset
    timeseries, y = load_robot_execution_failures()

    # Extract the features from the single pattern
    # extracted_features = impute(extract_features(
    #     timeseries, column_id="id", column_sort="time"
    # ))

    features_filtered_direct = extract_relevant_features(timeseries, y,
                                                     column_id='id', column_sort='time')
    
    # filtered_features = select_features(
    #     extracted_features, y
    # )

    # df = extract_relevant_features(timeseries, y, column_id='id', column_sort='time')
    # filtered_features.to_csv('filtered_features.csv')
    
    # relevance_table = calculate_relevance_table(
    #     extracted_features, y
    # )
    features_filtered_direct.to_csv('extracted_features.csv')

    return extracted_features
    
if __name__ == "__main__":
    my_extraction()