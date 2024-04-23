import tkinter as tk
from tkinter import ttk

def on_combobox_select(event):
    selected_value = combobox.get()
    text_display.config(state=tk.NORMAL)
    text_display.delete(1.0, tk.END)
    text_display.insert(tk.END, f"You selected {selected_value}.")
    text_display.config(state=tk.DISABLED)
    
def open_gui():
    # 创建主窗口
    root = tk.Tk()
    root.title("Button GUI")

    # 创建下拉栏并设置选项
    options = ["acc", "basketball", "HMP"]
    selected_option = tk.StringVar(value=options[0])
    combobox = ttk.Combobox(root, values=options, textvariable=selected_option)
    combobox.grid(row=0, column=0, padx=10, pady=10)
    combobox.bind("<<ComboboxSelected>>", on_combobox_select)

    # 创建文本显示器
    text_display = tk.Text(root, height=5, width=30, state=tk.DISABLED)
    text_display.grid(row=3, columnspan=3, padx=5, pady=5)

    # 启动主循环
    root.mainloop()
