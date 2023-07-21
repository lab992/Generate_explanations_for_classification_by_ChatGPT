import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def read_file():
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

    X_train = train_data.iloc[:, 1:]
    X_test = test_data.iloc[:, 1:]
    y_train = train_data.iloc[:, 0]
    y_test = test_data.iloc[:, 0]
    return X_train, X_test, y_train, y_test
    