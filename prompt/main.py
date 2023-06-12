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

    # Store a list of context or query, preparing for combining as a prompt later
    context = []
    query = []

    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)
        class_name, type = get_class_and_type(file_name)
        string = format_context_or_query(file_path, class_name, type)
        if (type == "learn"):
            context.append(string)
        else:
            query.append(string)

    prompt_query = "Now classify following data. The format should be: [Column 1, Column 2, ...] -- Class"
    result = "\n".join(context) + prompt_query + "\n".join(query)
    write_string_to_file(result, class_name, type)

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

# Format data to context or query
def format_context_or_query(file_path, class_name, type):
    transposed_matrix = txt_to_matrix(file_path)
    prompt_result = ""
    if (type == "learn"):
        prompt_context = "There are " + str(len(transposed_matrix[0])) + " " + class_name + ", and each has " + str(len(transposed_matrix)) + " columns."
        prompt_result += prompt_context
    data = format_data(file_path)
    prompt_result += data
    return prompt_result

# Transfer matrix to prompt
# Add detailed number to each column description
def format_data(file_path):
    transposed_matrix = txt_to_matrix(file_path)
    prompt_data = ""
    for i in range(len(transposed_matrix)):
        temp_string = "Each column " + str(i + 1) + " is " + ",".join(map(str, transposed_matrix[i])) + ". "
        prompt_data += temp_string
    return prompt_data

# Transfer txt to matrix, then transpose it to get each column 
def txt_to_matrix(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        matrix = [list(map(float, line.strip().split())) for line in lines]
        transposed_matrix = np.transpose(matrix)
        return transposed_matrix

# Type means train set or test set
def write_string_to_file(string, class_name, type):
    file_path = "prompt_" + class_name + ".txt"
    with open(file_path, 'w') as file:
        file.write(string)

if __name__ == "__main__":
    prompt()