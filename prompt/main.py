import os
import numpy as np
import tkinter as tk
import openai
import time
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
    role = "You are a data analyst, your job is to classify the given time series dataset."
    context_description = ""
    context_data_matrix = []
    context_data_label = []
    context_data = ""
    query = ""
    test_label = []

    for file_path in files:
        # Get the class name of train set
        file_name = os.path.basename(file_path)
        class_name, type, target = get_class_and_type_and_target(file_name)
        if (type == LEARN and target == X):
            context_description += format_context(file_path, class_name)
            context_data_matrix.extend(txt_to_matrix(file_path))
        elif (type == LEARN and target == Y):
            context_data_label.extend(txt_to_matrix(file_path))
        elif (type == TEST and target == X):
            query += format_query(file_path)
        elif (type == TEST and target == Y):
            test_label.extend(txt_to_array(file_path))
        else:
            raise ValueError("Wrong File")
    context_data += format_data(context_data_matrix, context_data_label)
    # result = context_data + context_label + "\n" + query
    # write_string_to_file(result, class_name)    
    return role + "\n" + context_description + "\n" + context_data, query, test_label


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
        class_name += string[:-2]
    elif class_name.endswith("Y"):
        target += Y
        class_name += string[:-2]
    else:
        raise ValueError("Wrong File name")
    return class_name, type, target

# Format data to context
def format_context(file_path, class_name):
    matrix = txt_to_matrix(file_path)
    prompt_description = "There are " + str(len(matrix)) + " " + class_name + ", and each has " + str(len(matrix[0])) + " columns.\n"
    prompt_format = "The dataset will be given in format: [column 1, column 2, ..., column "+ str(len(matrix[0])) +", label]."
    return prompt_description + prompt_format

# Format data to query
def format_query(file_path):
    prompt_query = "Try to classify following\n"
    with open(file_path, "r") as file:
        test = file.read()
        lines = test.split('\n')
        num_lines = len(lines) - 1
        prompt_query += test
        prompt_query += "to Label 0.0 or 1.0, with the help of dataset given above. Don't show me the code. "
        prompt_query += "Give me the label in format: [label 1, label 2, ..., label " + str(num_lines) +"]."
        return prompt_query

# Transfer matrix to prompt
# Add detailed number to each column description
def format_data(context_data_matrix, context_data_label):
    prompt_data = context_data_matrix[:]
    assert len(context_data_matrix) == len(context_data_label)
    # it seems that this step modify original data, fix it later
    for i in range(len(context_data_matrix)):
        prompt_data[i].append(context_data_label[i][0])

    string_matrix = ""
    for row in prompt_data:
        row_str = "[" + ",".join(str(element) for element in row) + "]"
        string_matrix += row_str + "\n"

    return string_matrix

# def format_label(file_path):
#     transposed_matrix = txt_to_matrix(file_path)
#     prompt_data = "Each class is "
#     for i in range(len(transposed_matrix)):
#         temp_string = ",".join(map(str, transposed_matrix[i])) + ". "
#         prompt_data += temp_string
#     return prompt_data

# Transfer txt to matrix, then transpose it to get each column 
def txt_to_matrix(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        matrix = [list(map(float, line.strip().split())) for line in lines]
        # transposed_matrix = np.transpose(matrix)
        return matrix

# Type means train set or test set
def write_string_to_file(string, class_name):
    file_path = "prompt_" + class_name + ".txt"
    with open(file_path, 'w') as file:
        file.write(string)

def label_result_to_array(string):
    stripped_string = string.strip("[]")
    elements = stripped_string.split(", ")
    array = [float(element) for element in elements]
    return array

def txt_to_array(file_path):
    array = []
    with open(file_path, "r") as file:
        for line in file:
            value = float(line.strip())
            array.append(value)
        return array

def false_rate(array1, array2):
    assert len(array1) == len(array2)
    count = sum([1 for a, b in zip(array1, array2) if a != b])
    result = count / len(array1)
    percentage = round(result * 100, 4)
    return f"{percentage}%"

if __name__ == "__main__":
    openai.api_key = "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"

    context, query, test_label = prompt()
    print(context)
    print(query)

    # print(completion.choices[0].message["content"])
    # print(false_rate(label_result_to_array(completion.choices[0].message["content"]), test_label))

    # count = 0

    # while (count < 8):
    #     try:
    #         completion = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "system", "content": context},
    #                 {"role": "user", "content": query},
    #             ]
    #         )

    #         gpt_result = label_result_to_array(completion.choices[0].message["content"])

    #         if (len(gpt_result) != len(test_label)):
    #             continue

    #         filename = "fertility2.txt"

    #         with open(filename, "a") as file:
    #             file.write(', '.join(map(str, gpt_result)))
    #             file.write("\n")
            
    #         count += 1
    #         print("ok")
    #         time.sleep(25)
    #     except ValueError:
    #         print("error")
    #         pass
    #     except Exception as e:
    #         raise e


    
    


