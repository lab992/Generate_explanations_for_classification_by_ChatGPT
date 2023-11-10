import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

def prompt_gen():
    train_data, test_data = feature_gen()
    return context_gen(train_data), query_gen(test_data)

def context_gen(train_data):
    role = "You are a data analyst, your job is to classify time series by the given features."
    background = ("The gesture acquisition device is a Nintendo Wiimote remote controller with built-in three-axis accelerometer."
                    "Data is acceleration in x-axis dimension. It is classified to 3 gestures"
                    )
    classes = ("The gestures are (class label - English translation): "
                # "1 – pick-up"
                "2 – shake"
                "3 – one move to the right"
                "4 – one move to the left"
                # "5 – one move to up"
                # "6 – one move to down"
                # "7 – one left circle"
                # "8 – one right circle"
                # "9 – one move toward the screen"
                # "10 – one move away from the screen"
                )
    
    # decision tree
    # features = ("The dataset has 11 columns. The first column is label and the rest are 3 features in order: "
    #             'standard_deviation, '
    #             'number_crossing_m__m_1, '
    #             'fft_coefficient__attr_"angle"__coeff_1, '
    #             'fourier_entropy__bins_5, '
    #             'linear_trend__attr_"slope", '
    #             'fourier_entropy__bins_2, '
    #             'range_count__max_0__min_-1000000000000.0, '
    #             'autocorrelation__lag_5, '
    #             'index_mass_quantile__q_0.4, '
    #             'mean_n_absolute_max__number_of_maxima_7. '
                # )
    # features = ("The dataset has 4 columns. The first column is lable and the rest are 3 features in order: "
    #         'number_crossing_m__m_1, '
    #         'agg_linear_trend__attr_"intercept"__chunk_len_5__f_agg_"min", '
    #         'range_count__max_1000000000000.0__min_0. '
    #         )
    features = ("The dataset has 11 columns. The first column is lable and the rest are 10 features in order. ")

    # Gradient
    # features = ("The dataset has 11 columns. The first column is label and the rest are 10 features in order: "
    #         'cid_ce__normalize_False, '
    #         'agg_linear_trend__attr_"slope"__chunk_len_10__f_agg_"var", '
    #         'cwt_coefficients__coeff_4__w_20__widths_(2, 5, 10, 20), '
    #         'linear_trend__attr_"pvalue", '
    #         'permutation_entropy__dimension_7__tau_1, '
    #         'fft_coefficient__attr_"real"__coeff_5, '
    #         'agg_linear_trend__attr_"stderr"__chunk_len_5__f_agg_"var", '
    #         'root_mean_square, '
    #         'number_crossing_m__m_1, '
    #         'change_quantiles__f_agg_"var"__isabs_True__qh_1.0__ql_0.4. '
    #         )

    # Random Forest
    # features = ("The dataset has 11 columns. The first column is label and the rest are 10 features in order: "
    #     'fft_coefficient__attr_"imag"__coeff_1, '
    #     'abs_energy, '
    #     'root_mean_square, '
    #     'fourier_entropy__bins_5, '
    #     'standard_deviation, '
    #     'fourier_entropy__bins_2, '
    #     'fourier_entropy__bins_10, '
    #     'fourier_entropy__bins_100, '
    #     'absolute_sum_of_changes, '
    #     'agg_autocorrelation__f_agg_"var"__maxlag_40. '
    #     )
                
    data_description = ("Following is the dataset of 60 data: \n")
    
    # 280 tokens
    # 预留 1000 token给query和回答
    # 每个数字3 token，大概4位有效数字

    return role + "\n" + background + "\n" + classes + "\n" + features + "\n" + data_description + "\n" + feature_to_txt(train_data)

def query_gen(test_data):
    task = ("Try to classify following 15 data to these 3 classes, with the help of dataset given above."
            "The following data have no lable. They have only 10 features. You should classify them to lable 2, 3, or 4."
               "You should not show the code but give the answer directly."
               "You must give me the label in format: [label 1, label 2, ..., label 15]"
               "You must check whether there are exactly 15 labels in your answer." + "\n")
    return task + feature_to_txt(test_data)

def feature_gen():
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    train_file = filedialog.askopenfilename()
    train_data = pd.read_csv(train_file)

    test_file = filedialog.askopenfilename()
    test_data = pd.read_csv(test_file)

    # 去除id
    train_data = train_data.iloc[: , 1:].iloc[list(range(0,20)) + list(range(30,50)) + list(range(60,80))]
    test_data = test_data.iloc[: , 1:].iloc[list(range(5,10)) + list(range(75,80)) + list(range(145,150))]

    # 定义格式化函数
    def format_number(num):
        formatted_num = float(f'{num:.4f}')  # 格式化为保留四位小数
        return format(formatted_num, ".4g")
    
    formatted_train_data = train_data.applymap(format_number)
    formatted_test_data = test_data.applymap(format_number)

    # 使用 apply 函数将每一行转换为数组
    train_array_series = formatted_train_data.apply(lambda row: row.to_numpy(), axis=1)
    test_array_series = formatted_test_data.apply(lambda row: row.to_numpy(), axis=1)

    # 将包含数组的 Series 转换为列表
    train_array_list = train_array_series.tolist()
    test_array_list = test_array_series.tolist()

    for i in range(0, len(train_array_list)):
        start_value = 2
        if i < 20 :
            start_value += 0
        elif i < 40:
            start_value += 1
        else:
            start_value += 2

        train_array_list[i] = np.insert(train_array_list[i], 0, str(start_value))

    return train_array_list, test_array_list

def feature_to_txt(array_list):
    result = ""
    # 打印带有所需格式的列表
    for array in array_list:
        formatted_string = '[' + ' '.join(array) + ']'+ '\n'
        result += formatted_string
    return result

class PromptGenerator:

    def __init__(self, X_train, X_test, y_train):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train

    def prompt_generator(context, query):
        pass