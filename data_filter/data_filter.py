import tkinter as tk
from tkinter import filedialog
import pandas as pd

def filter():
    root = tk.Tk()
    root.withdraw()

    # Open file selection window
    files = filedialog.askopenfilename()
    data = pd.read_table(files, sep = '\s+', header=None).round(decimals=2)
    for i in range(10):
        df = data.iloc[i * 30 : i * 30 + 30]
        df.to_csv(str(i) + '_output.txt', sep = ',', index = False, header=None)

    print("OK")

if __name__ == "__main__":
    filter() 