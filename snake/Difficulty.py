from tkinter import ttk
from snake.style import Style
from snake.GameFrame import *
from snake.GameFrame import change_speed


class Difficulty(ttk.Frame):
    def __init__(self, container, controller, speed=75):
        super().__init__(container)

        style = Style()
        pad_y = (0, 10)

        button_easy = ttk.Button(self, text="\nEasy\n", command=lambda:
                                 [controller.show_frame(GameFrame), change_speed(100)])
        button_easy.grid(row=1, column=0, pady=pad_y)

        button_medium = ttk.Button(self, text="\nMedium\n", command=lambda:
                                 [controller.show_frame(GameFrame), change_speed(75)])
        button_medium.grid(row=2, column=0, pady=pad_y)

        button_hard = ttk.Button(self, text="\nHard\n", command=lambda:
                                 [controller.show_frame(GameFrame), change_speed(50)])
        button_hard.grid(row=3, column=0, pady=pad_y)

