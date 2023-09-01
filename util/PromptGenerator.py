import tkinter as tk
from tkinter import filedialog
import pandas as pd

def prompt_gen():
    train_data, test_data = feature_gen()
    return context_gen(train_data), query_gen(test_data)

def context_gen(train_data):
    role = "You are a data analyst, your job is to classify time series by the given features."
    background = ("The gesture acquisition device is a Nintendo Wiimote remote controller with built-in three-axis accelerometer."
                    "Data is acceleration in x-axis dimension. It is classified to 4 gestures"
                    )
    classes = ("The gestures are (class label - English translation): "
                "1 – pick-up"
                "2 – shake"
                "3 – one move to the right"
                "4 – one move to the left"
                )
    features = ("The dataset has 11 columns. The first column is label and the rest are 10 features in order: "
                'standard_deviation, '
                'number_crossing_m__m_1, '
                'fft_coefficient__attr_"angle"__coeff_1, '
                'fourier_entropy__bins_5, '
                'linear_trend__attr_"slope", '
                'fourier_entropy__bins_2, '
                'range_count__max_0__min_-1000000000000.0, '
                'autocorrelation__lag_5, '
                'index_mass_quantile__q_0.4, '
                'mean_n_absolute_max__number_of_maxima_7. '
                )
                
    data_description = ("Following is the dataset of 300 data: \n")
    
    # 280 tokens
    # 预留 1000 token给query和回答
    # 每个数字3 token，大概4位有效数字

    return role + "\n" + background + "\n" + classes + "\n" + features + "\n" + data_description + "\n" + feature_to_txt(train_data)

def query_gen(test_data):
    task = ("Try to classify following 20 data to these 4 labels, with the help of dataset given above."
               "You should not show the code but give the answer directly."
               "You must give me the label in format: [label 1, label 2, ..., label 20]"
               "You must check whether there are exactly 20 labels in your answer." + "\n")
    return task + feature_to_txt(test_data)

def feature_gen():
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    file = filedialog.askopenfilename()
    data = pd.read_csv(file)

    # 去除id
    data = data.iloc[: , 1:]

    # 取三分之一
    # train_rows = pd.concat([data.iloc[0:15], 
    #                            data.iloc[30:45], 
    #                            data.iloc[60:75],
    #                            data.iloc[90:105], 
    #                            data.iloc[120:135]
    #                            ])
    
    # test_rows = pd.concat([data.iloc[20:25], 
    #                            data.iloc[50:55], 
    #                            data.iloc[80:85],
    #                            data.iloc[110:115], 
    #                            data.iloc[140:145]
    #                            ])

    # 定义格式化函数
    def format_number(num):
        formatted_num = float(f'{num:.4f}')  # 格式化为保留四位小数
        return format(formatted_num, ".4g")
    
    formatted_data = data.applymap(format_number)

    # 使用 apply 函数将每一行转换为数组
    array_series = formatted_data.apply(lambda row: row.to_numpy(), axis=1)

    # 将包含数组的 Series 转换为列表
    array_list = array_series.tolist()

    train_data = array_list[0:15] + array_list[30:45] + array_list[60:75] + array_list[90:105]
    test_temp_data = array_list[20:25] + array_list[50:55] + array_list[80:85] + array_list[110:115]
    test_data = [array[1:] for array in test_temp_data]

    return train_data, test_data

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