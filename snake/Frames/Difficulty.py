from tkinter import ttk
from snake.Frames.style import Style


class Difficulty(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        style = Style()
        pad_y = (0, 10)

        button_easy = ttk.Button(self, text="\nEasy\n")
        button_easy.grid(row=1, column=0, pady=pad_y)

        button_medium = ttk.Button(self, text="\nMedium\n")
        button_medium.grid(row=2, column=0, pady=pad_y)

        button_hard = ttk.Button(self, text="\nHard\n")
        button_hard.grid(row=3, column=0, pady=pad_y)
