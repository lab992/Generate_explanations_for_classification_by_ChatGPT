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
            single_array.append(int(round(num * 10, 0)))
            j += intervall
        average_array.append(single_array)
    
    # for i in range(4):
    #     df = average_array[i * 30 : i * 30 + 30]
    #     with open(str(i + 1) + '_origin_avg_4.txt', "a") as file:
    #         for j in range(len(df)):
    #             file.write(str(df[j]))
    #             file.write("\n")

    with open('class_4_avg_2.txt', "a") as file:
        for j in range(len(average_array[210:260])):
            file.write(str(average_array[j + 210]))
            file.write("\n")
    return average_array

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

    df = []
    df.extend(trend[0:10])
    df.extend(trend[30:40])
    df.extend(trend[80:90])
    df.extend(trend[110:120])
    with open('class_3_avg_2.txt', "a") as file:
        for j in range(len(df)):
            file.write(str(df[j]))
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
    

if __name__ == "__main__":
    average(2) 