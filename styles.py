from tkinter import ttk


def apply_styles():
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), foreground='blue')
    style.configure('TListbox', font=('Helvetica', 12), background='black')
    style.configure('TFrame', background='lightgray')