import numpy as np
import tkinter as tk
from tkinter import filedialog

def txt_to_array():
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    file = filedialog.askopenfilename()

    array = []
    with open(file, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                array.append([float(x) for x in line.split(',')])
    return array

def false_rate(array1, array2):
    count = sum([1 for a, b in zip(array1, array2) if a != b])
    result = count / len(array1)
    percentage = round(result * 100, 4)
    return f"{percentage}%"

if __name__ == "__main__": 
    target1 = [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0]
    target2 = [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    array = []
    array.append(txt_to_array())
    for i in range(len(array[0])):
        print(false_rate(target2, array[0][i]))
