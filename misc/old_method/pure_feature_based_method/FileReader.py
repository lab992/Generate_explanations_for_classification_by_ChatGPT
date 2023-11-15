import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def read_file_acc():
    # Create main window
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilenames()

    # Set the maximum allowed file count
    max_allowed_files = 2

    if len(files) != max_allowed_files:
        raise ValueError("Wrong file number.")
    
    train_data = None
    test_data = None

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

    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)

        if file_name.endswith("TRAIN.txt"):
            train_data = pd.read_table(file_path, sep = '\s+', header=None)
        elif file_name.endswith("TEST.txt"):
            test_data = pd.read_table(file_path, sep = '\s+', header=None)
        else:
            raise ValueError("Wrong file.")
        
    train_data = train_data.iloc[30:120]
    test_data = test_data.iloc[70:280]
    structured_train = data_format_acc(train_data, 30)
    structured_test = data_format_acc(test_data, 70)
    X_train = structured_train.iloc[:, 1:]
    X_test = structured_test.iloc[:, 1:]
    y_train = train_data.iloc[:, 0]
    y_test = test_data.iloc[:, 0]
    
    return X_train, X_test, y_train, y_test
    


def read_file_basket():
    # Create main window
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilenames()

    result = None
    y = []

    def file_name_classifier(file_name):
        split = file_name[:-4].split('_')
        user = split[0]
        frequency = split[1][-1]
        label = split[1][:-1]
        return user, frequency, label
    
    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)

        user, frequency, label = file_name_classifier(file_name)

        df = pd.read_table(file_path, skiprows=3, sep = ',')

        num_rows = len(df)
        df['User'] = [user] * num_rows
        df['Frequency'] = [frequency] * num_rows
        # df['Label'] = [label] * num_rows

        result = pd.concat([result, df])
        y.append(label)
    
    result['id'] = (result['Frequency'] != result['Frequency'].shift()).cumsum() - 1

    new_df = result[['id', 'Time (s)', ' X (m/s2)']]

    new_df = new_df.dropna().reset_index(drop=True)

    result_y = pd.Series(y)

    return new_df, result_y


        
def read_file_HMP():
    # 创建主窗口
    root = tk.Tk()
    root.withdraw()

    # 选择文件夹按钮的回调函数
    folders = []

    while True:
        folder = filedialog.askdirectory()
        if not folder:
            break  # 用户点击取消
        folders.append(folder)
    for folder in folders:
        print("Selected folder:", folder)

    result = None
    y = []

    # 处理选择的文件夹
    file_pair = []

    for folder_path in folders:
        folder_name = os.path.basename(folder_path)

        # 遍历文件夹中的所有文件
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                file_pair.append((folder_name, file_path))

    print('ok')

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

