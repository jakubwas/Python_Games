import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sudoku")
        self.resizable(False, False)
        self.geometry("500x500")
        self.sudoku_frame = ttk.Frame(self)
        self.button_frame = ttk.Frame(self)
        self.width = 8
        self.iheight = 10
        self.number = tk.StringVar()

        # (0,0)
        entry00_1 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_2 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_3 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_4 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_5 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_6 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_7 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_8 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry00_9 = ttk.Entry(self, textvariable=self.number, width=self.width)

        entry00_1.grid(row=0, column=0, sticky="WE", ipady=self.iheight)
        entry00_2.grid(row=0, column=1, sticky="WE", ipady=self.iheight)
        entry00_3.grid(row=0, column=2, sticky="WE", ipady=self.iheight)
        entry00_4.grid(row=1, column=0, sticky="WE", ipady=self.iheight)
        entry00_5.grid(row=1, column=1, sticky="WE", ipady=self.iheight)
        entry00_6.grid(row=1, column=2, sticky="WE", ipady=self.iheight)
        entry00_7.grid(row=2, column=0, sticky="WE", ipady=self.iheight)
        entry00_8.grid(row=2, column=1, sticky="WE", ipady=self.iheight)
        entry00_9.grid(row=2, column=2, sticky="WE", ipady=self.iheight)

        # (0,1)
        entry01_1 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_2 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_3 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_4 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_5 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_6 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_7 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_8 = ttk.Entry(self, textvariable=self.number, width=self.width)
        entry01_9 = ttk.Entry(self, textvariable=self.number, width=self.width)

        entry01_1.grid(row=0, column=3, sticky="WE", ipady=self.iheight)
        entry01_2.grid(row=0, column=4, sticky="WE", ipady=self.iheight)
        entry01_3.grid(row=0, column=5, sticky="WE", ipady=self.iheight)
        entry01_4.grid(row=1, column=3, sticky="WE", ipady=self.iheight)
        entry01_5.grid(row=1, column=4, sticky="WE", ipady=self.iheight)
        entry01_6.grid(row=1, column=5, sticky="WE", ipady=self.iheight)
        entry01_7.grid(row=2, column=3, sticky="WE", ipady=self.iheight)
        entry01_8.grid(row=2, column=4, sticky="WE", ipady=self.iheight)
        entry01_9.grid(row=2, column=5, sticky="WE", ipady=self.iheight)


root = MainWindow()
root.mainloop()
