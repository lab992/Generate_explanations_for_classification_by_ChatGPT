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

    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)

        if file_name.endswith("TRAIN.txt"):
            train_data = pd.read_table(file_path, sep = '\s+', header=None)
        elif file_name.endswith("TEST.txt"):
            test_data = pd.read_table(file_path, sep = '\s+', header=None)
        else:
            raise ValueError("Wrong file.")

    structured_train = data_format_acc(train_data)
    structured_test = data_format_acc(test_data)
    X_train = structured_train.iloc[:, 1:]
    X_test = structured_test.iloc[:, 1:]
    y_train = train_data.iloc[:, 0]
    y_test = test_data.iloc[:, 0]
    
    return X_train, X_test, y_train, y_test
    
def data_format_acc(data):
    num_rows, num_columns = data.shape
    result = pd.DataFrame(columns=['lable', 'id', 'time', 'acceleration'])
    for i in range(num_rows):
        row = data.iloc[i]
        df = pd.DataFrame({
            'lable': [row[0]] * len(row[1:]),
            'id': [i] * len(row[1:]),
            'time': [i * 0.1 for i in range(len(row[1:]))],
            'acceleration': row[1:]               
        })
        result = pd.concat([result, df])
    result = result.dropna().reset_index(drop=True)
    return result

def read_file_basket():
    # Create main window
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilenames()

    result = None

    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)

        user, frequency, label = file_name_classifier(file_name)

        df = pd.read_table(file_path, skiprows=3, sep = ',')

        num_rows = len(df)
        df['User'] = [user] * num_rows
        df['Frequency'] = [frequency] * num_rows
        df['Label'] = [label] * num_rows

        result = pd.concat([result, df])
    
    result = result.dropna().reset_index(drop=True)

    print("ok")
    return result

        
def file_name_classifier(file_name):
    split = file_name[:-4].split('_')
    user = split[0]
    frequency = split[1][-1]
    label = split[1][:-1]
    return user, frequency, label