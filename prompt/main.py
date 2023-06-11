import os
import numpy as np
import tkinter as tk
from tkinter import filedialog

def prompt():
    # Create main window
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilenames()

    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)
        class_name, type = get_class_and_type(file_name)
        string = format_prompt(file_path, class_name)
        write_string_to_file(string, class_name, type)

# Deal with the name of file
# Decide the type of prompt by suffix
# Get the name of class by prefix
def get_class_and_type(string):
    if string.endswith('learn.txt'):
        return string[:-9], "learn"
    elif string.endswith('test.txt'):
        return string[:-8], "test"
    else:
        raise ValueError("Wrong File name")

# Format data to prompt
# First transfer txt to matrix, then transpose to get each column
# Prefix contains the information of class name and number of columns
# Then add detailed number to each column description
def format_prompt(file_path, class_name):
    with open(file_path, "r") as file:
        lines = file.readlines()
        matrix = [list(map(float, line.strip().split())) for line in lines]
        transposed_matrix = np.transpose(matrix)
        prompt_prefix = "There are " + str(len(matrix)) + " " + class_name + ", and each has " + str(len(transposed_matrix)) + " columns."
        for i in range(len(transposed_matrix)):
            temp_string = "Each column " + str(i + 1) + " is " + ",".join(map(str, transposed_matrix[i])) + ". "
            prompt_prefix += temp_string
        return prompt_prefix

# Type means train set or test set
def write_string_to_file(string, class_name, type):
    file_path = "prompt_" + class_name + "_" + type + ".txt"
    with open(file_path, 'w') as file:
        file.write(string)

if __name__ == "__main__":
    prompt()