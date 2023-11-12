import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

def filter():
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilename()
    data = pd.read_table(files, sep = '\s+', header=None).round(decimals=2)
    for i in range(1):
        df = data.iloc[i * 30 : i * 30 + 30]
        df.to_csv(str(i) + '_output.txt', sep = ' ', index = False, header=None)

def average(intervall):
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilename()
    data = pd.read_table(files, sep = '\s+', header=None)
    # delete label 
    data = data.iloc[:, 1:]

    # impute to [0,1]
    array = data.to_numpy()
    min_max = []

    # min-max
    for i in range(len(array)):
        max_x = max(array[i])
        min_x = min(array[i])
        temp_array = [round((j - min_x)/(max_x - min_x), 2) for j in array[i]]
        min_max.append(temp_array)

    average_array = []
    for i in range(len(min_max)):
        j = 0
        single_array = []
        while (not (np.isnan(min_max[i][j + intervall]))):
            num = (sum(min_max[i][j : j + intervall])) / intervall
            single_array.append(int(round(num * 9, 0)))
            j += intervall
        average_array.append(single_array)
    
    # df1 = average_array[30:60]
    # df2 = average_array[60:90]
    # df3 = average_array[90:120]

    result = average_array[70:90] + average_array[140:160] + average_array[210:230]

    return result

    # result_array_1 = [trim_sequence(subarray) for subarray in df1]
    # result_array_2 = [trim_sequence(subarray) for subarray in df2]
    # result_array_3 = [trim_sequence(subarray) for subarray in df3]

    # with open('class_2_trend_2.txt', "a") as file:
    #     for j in range(len(df1)):
    #         file.write(str(df1[j]))
    #         file.write("\n")
    
    # with open('class_3_trend_2.txt', "a") as file:
    #     for j in range(len(df2)):
    #         file.write(str(df2[j]))
    #         file.write("\n")

    # with open('class_4_trend_2.txt', "a") as file:
    #     for j in range(len(df3)):
    #         file.write(str(df3[j]))
    #         file.write("\n")

    with open('class_2_average_2_modified.txt', "a") as file:
        for j in range(len(result_array_1)):
            file.write(str(result_array_1[j]))
            file.write("\n")
    
    with open('class_3_average_2_modified.txt', "a") as file:
        for j in range(len(result_array_2)):
            file.write(str(result_array_2[j]))
            file.write("\n")

    with open('class_4_average_2_modified.txt', "a") as file:
        for j in range(len(result_array_3)):
            file.write(str(result_array_3[j]))
            file.write("\n")

def transformer(intervall):
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilename()
    data = pd.read_table(files, sep = '\s+', header=None)
    # delete label 
    data = data.iloc[:, 1:]

    # impute to [0,1]
    array = data.round(decimals=2).to_numpy()
    min_max = []
    # min-max
    for i in range(len(array)):
        max_x = max(array[i])
        min_x = min(array[i])
        temp_array = [round((j - min_x)/(max_x - min_x), 2) for j in array[i]]
        min_max.append(temp_array)

    trend = []
    for i in range(len(min_max)):
        j = 0
        single_array = []
        while (not (np.isnan(min_max[i][j + intervall]))):
            num = (min_max[i][j + intervall] - min_max[i][j]) / intervall
            single_array.append(int(round(num * 100, 0)))
            j += intervall
        trend.append(single_array)

    # for i in range(len(trend) / 30):
    #     df = trend[i * 30 : i * 30 + 30]
    #     with open(str(i + 1) + '_test.txt', "a") as file:
    #         for j in range(len(df)):
    #             file.write(str(df[j]))
    #         file.write("\n")

    df1 = trend[30:60]
    df2 = trend[60:90]
    df3 = trend[90:120]

    result_array_1 = [trim_sequence(subarray) for subarray in df1]
    result_array_2 = [trim_sequence(subarray) for subarray in df2]
    result_array_3 = [trim_sequence(subarray) for subarray in df3]

    # with open('class_2_trend_2.txt', "a") as file:
    #     for j in range(len(df1)):
    #         file.write(str(df1[j]))
    #         file.write("\n")
    
    # with open('class_3_trend_2.txt', "a") as file:
    #     for j in range(len(df2)):
    #         file.write(str(df2[j]))
    #         file.write("\n")

    # with open('class_4_trend_2.txt', "a") as file:
    #     for j in range(len(df3)):
    #         file.write(str(df3[j]))
    #         file.write("\n")

    with open('class_2_trend_2_modified.txt', "a") as file:
        for j in range(len(result_array_1)):
            file.write(str(result_array_1[j]))
            file.write("\n")
    
    with open('class_3_trend_2_modified.txt', "a") as file:
        for j in range(len(result_array_2)):
            file.write(str(result_array_2[j]))
            file.write("\n")

    with open('class_4_trend_2_modified.txt', "a") as file:
        for j in range(len(result_array_3)):
            file.write(str(result_array_3[j]))
            file.write("\n")


    # 转化成UND
    # result = []
    # for i in range(len(trend)):
    #     result_list = []
    #     for j in trend[i]:
    #         if j > 0:
    #             result_list.append("U" + '{:g}'.format(abs(j)))
    #         if j == 0:
    #             result_list.append("N")
    #         else:
    #             result_list.append("D" + '{:g}'.format(abs(j)))
    #     result.append(result_list)        
    

def trim_sequence(arr):
    sequence_to_remove = [0, -1, 1, -2, 2]

    # 找到子数组开头不是序列的索引
    start_index = 0
    while start_index < len(arr) and arr[start_index] in sequence_to_remove:
        start_index += 1

    # 找到子数组结尾不是序列的索引
    end_index = len(arr) - 1
    while end_index >= 0 and arr[end_index] in sequence_to_remove:
        end_index -= 1

    # 返回去掉序列后的子数组
    return arr[start_index:end_index + 1]

if __name__ == "__main__":
    average(2)