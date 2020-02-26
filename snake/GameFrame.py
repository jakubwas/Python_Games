from tkinter import ttk
from snake.Snake import Snake

SPEED = 75


def change_speed(speed):
    global SPEED
    SPEED = speed


class GameFrame(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.bind_all("<Key>", self.on_key_press)


    def on_key_press(self, e):
        key = e.keysym
        if key == "a":
            snake_obj = Snake(SPEED)
            snake_obj.grid()
