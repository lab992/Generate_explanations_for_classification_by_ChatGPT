import os
import glob
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import random

def read_file_acc():

    train_data = None
    test_data = None

    train_data = pd.read_table('selected_dataset/acc/AllGestureWiimoteX_TRAIN.txt', sep = '\s+', header=None)
    test_data = pd.read_table('selected_dataset/acc/AllGestureWiimoteX_TEST.txt', sep = '\s+', header=None)

    def data_format_acc(data, bias):
        num_rows, num_columns = data.shape
        result = pd.DataFrame(columns=['lable', 'id', 'time', 'acceleration'])
        for i in range(num_rows):
            row = data.iloc[i]
            df = pd.DataFrame({
                'lable': [row[0]] * len(row[1:]),
                'id': [i + bias] * len(row[1:]),
                'time': [i * 0.1 for i in range(len(row[1:]))],
                'acceleration': row[1:]               
            })
            result = pd.concat([result, df])
        result = result.dropna().reset_index(drop=True)
        return result
    
    def random_disturb(row):
        max_values = row.max()
        min_values = row.min()
        noise = np.random.normal(0.007 * min_values, 0.007 * max_values, size=len(row))
        return noise + row
    
    def sudden_disturb(row):
        max_values = row.max()
        min_values = row.min()
        length = 50
        abrupt_noise = [0] * len(row)
        random_start = random.randint(0, len(row) - length - 1)

        for i in range(random_start, random_start + length):
            abrupt_noise[i] += 0.04 * (max_values - min_values)

        series_with_abrupt_noise = row + abrupt_noise
        return series_with_abrupt_noise

    # def periodic_disturb(row):
    #     period = 24  
    #     periodic_noise = 0.2 * np.sin(2 * np.pi * time / period)

    #     series_with_periodic_noise = series + periodic_noise    

    # Select Class 2,3,4
    train_data = train_data.iloc[30:120]
    # test_data = test_data.iloc[70:280]
    test_data = test_data.iloc[list(range(70,90)) + list(range(140,160)) + list(range(210,230))]

    robust_train_data = train_data.apply(sudden_disturb, axis=1)
    robust_test_data = test_data.apply(sudden_disturb, axis=1)

    structured_train = data_format_acc(robust_train_data, 30)
    structured_test = data_format_acc(robust_test_data, 70)

    # structured_train = data_format_acc(train_data, 30)
    # structured_test = data_format_acc(test_data, 70)

    # structured_train['lable'] = structured_train['lable'].replace({2: 'shake_hand', 3: 'move_to_left', 4: 'move_to_right'})
    # structured_test['lable'] = structured_test['lable'].replace({2: 'shake_hand', 3: 'move_to_left', 4: 'move_to_right'})

    X_train = structured_train.iloc[:, 1:]
    X_test = structured_test.iloc[:, 1:]
    y_train = train_data.iloc[:, 0]
    y_test = test_data.iloc[:, 0]
    
    return X_train, X_test, y_train, y_test
    


def read_file_basket():

    train_files = glob.glob(os.path.join('selected_dataset/basket/train', '*.txt'))
    test_files = glob.glob(os.path.join('selected_dataset/basket/test', '*.txt'))

    def file_name_classifier(file_name):
        split = file_name[:-4].split('_')
        user = split[0]
        frequency = split[1][-1]
        label = split[1][:-1]
        return user, frequency, label

    def read_dataset(files):

        result = None
        y = []
        for txt_file in files:
            # Get the class name of train set
            file_name = os.path.basename(txt_file)
            user, frequency, label = file_name_classifier(file_name)
            df = pd.read_table(txt_file, skiprows=3, sep = ',')

            num_rows = len(df)
            df['User'] = [user] * num_rows
            df['Frequency'] = [frequency] * num_rows

            result = pd.concat([result, df])
            y.append(label)
        
        result['id'] = (result['Frequency'] != result['Frequency'].shift()).cumsum() - 1
        new_df = result[['id', 'Time (s)', ' X (m/s2)']]
        new_df.rename(columns={'Time (s)': 'time', ' X (m/s2)': 'x'}, inplace=True)
        new_df = new_df.dropna().reset_index(drop=True)
        result_y = pd.Series(y)

        return new_df, result_y
    
    X_train, y_train = read_dataset(train_files)
    X_test, y_test = read_dataset(test_files)
    
    return X_train, X_test, y_train, y_test


        
def read_file_HMP():

    train_folders = []
    train_folders.append('selected_dataset/HMP/train/Descend_stairs')
    train_folders.append('selected_dataset/HMP/train/Comb_hair')
    train_folders.append('selected_dataset/HMP/train/Liedown_bed')

    test_folders = []
    test_folders.append('selected_dataset/HMP/test/Descend_stairs')
    test_folders.append('selected_dataset/HMP/test/Comb_hair')
    test_folders.append('selected_dataset/HMP/test/Liedown_bed')

    def read_folders(folders):
        result = None
        y = []
        file_pair = []

        for folder_path in folders:
            folder_name = os.path.basename(folder_path)

            # 遍历文件夹中的所有文件
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(folder_path, file_name)
                    file_pair.append((folder_name, file_path))

        for i in range(len(file_pair)):
            folder_name, file_path = file_pair[i]
            data = pd.read_table(file_path, sep = ' ', header=None)
            num_rows = len(data)
            df = pd.DataFrame({
                    # 'lable': [folder_name] * num_rows,
                    'id': [i] * num_rows,
                    'time': [i * 0.1 for i in range(num_rows)],
                    'x': data.iloc[:, 0]
                    # 'y': data.iloc[:, 1],
                    # 'z': data.iloc[:, 2]       
                })


            result = pd.concat([result, df])
            y.append(folder_name)

        result = result.dropna().reset_index(drop=True)
        result_y = pd.Series(y)
        return result, result_y
    
    X_train, y_train = read_folders(train_folders)
    X_test, y_test = read_folders(test_folders)
    return X_train, X_test, y_train, y_test



