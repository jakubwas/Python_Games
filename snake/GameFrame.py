from tkinter import ttk
from snake.Snake import Snake
import tkinter as tk
SPEED = 75


def change_speed(speed):
    global SPEED
    SPEED = speed


def on_key_press(e):
    key = e.keysym
    if key == "a":
        snake_obj = Snake(SPEED)
        snake_obj.grid()


class GameFrame(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label = tk.Label(self,
                         text="Press 'a' to start",
                         foreground="red",
                         background="black",
                         font=("Helvetica", 18, "bold", "italic")
                         )
        label.grid(row=0, column=0, sticky="NSEW")
        self.bind_all("<Key>", on_key_press)
