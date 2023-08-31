import numpy as np
from tsfresh import select_features, extract_relevant_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import select_features,extract_features
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def cal_features(X, y):

    extracted_features = extract_features(X, column_id="id", column_sort="Time (s)")
    # extracted_features = extract_features(X, column_id="id", column_sort="time")

    # extracted_features.to_csv('HMP_extracted.csv')

    impute(extracted_features)

    features_filtered = select_features(extracted_features, y)

    features_filtered.to_csv('BASKET_filtered.csv')

def n_features_selection():

    # 加载数据集（以鸢尾花数据集为例）
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    csv = filedialog.askopenfilename()
    txt = filedialog.askopenfilename()

    data = pd.read_csv(csv)

    features = pd.read_table(txt, header=None)
    array_features = features.values.flatten()
    array_columns = np.insert(array_features, 0, "target")

    selected = data[array_columns]

    selected.to_csv("gradient_selected.csv")




