import os
import numpy as np
import tkinter as tk
import openai
from tkinter import filedialog

X = 0
Y = 1
LEARN = 2
TEST = 3

def prompt():
    # Create main window
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilenames()

    # Store a list of context or query, preparing for combining as a prompt later
    context_data = ""
    context_class = ""
    query = ""

    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)
        class_name, type, target = get_class_and_type_and_target(file_name)
        if (type == LEARN and target == X):
            context_data += format_context(file_path, class_name)
        elif (type == LEARN and target == Y):
            context_class += format_class(file_path)
        elif (type == TEST and target == X):
            query += format_query(file_path)
        else:
            raise ValueError("Wrong File")
    result = context_data + "\n" + context_class + "\n" + query
    write_string_to_file(result, class_name)    
    return context_data + "\n" + context_class, query


# Deal with the name of file
# Decide the type of prompt by suffix
# Get the name of class by prefix
def get_class_and_type_and_target(string):
    class_name = ""
    type = 0
    target = 0
    if string.endswith("learn.txt"):
        class_name += string[:-9]
        type += LEARN
    elif string.endswith("test.txt"):
        class_name += string[:-8]
        type += TEST
    else:
        raise ValueError("Wrong File name")
    if class_name.endswith("X"):
        target += X
    elif class_name.endswith("Y"):
        target += Y
    else:
        raise ValueError("Wrong File name")
    return class_name, type, target

# Format data to context
def format_context(file_path, class_name):
    transposed_matrix = txt_to_matrix(file_path)
    prompt_context = "There are " + str(len(transposed_matrix[0])) + " " + class_name + ", and each has " + str(len(transposed_matrix)) + " columns.\n"
    data = format_data(file_path)
    prompt_context += data
    return prompt_context

# Format data to  query
def format_query(file_path):
    transposed_matrix = txt_to_matrix(file_path)
    prompt_query = "Now classify following " + str(len(transposed_matrix[0])) + " data to class 0.0 or 1.0.\n"
    data = format_data(file_path)
    prompt_query += data
    prompt_query += "\nGive me the answer"
    return prompt_query

# Transfer matrix to prompt
# Add detailed number to each column description
def format_data(file_path):
    transposed_matrix = txt_to_matrix(file_path)
    prompt_data = ""
    for i in range(len(transposed_matrix)):
        temp_string = "Each column " + str(i + 1) + " is " + ",".join(map(str, transposed_matrix[i])) + ".\n"
        prompt_data += temp_string
    return prompt_data

def format_class(file_path):
    transposed_matrix = txt_to_matrix(file_path)
    prompt_data = "Each class is "
    for i in range(len(transposed_matrix)):
        temp_string = ",".join(map(str, transposed_matrix[i])) + ". "
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
def write_string_to_file(string, class_name):
    file_path = "prompt_" + class_name + ".txt"
    with open(file_path, 'w') as file:
        file.write(string)

if __name__ == "__main__":
    openai.api_key = "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"

    context, query = prompt()

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": query},
        ]
    )

    print(completion.choices[0].message)