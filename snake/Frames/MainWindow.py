from tkinter import ttk
import tkinter as tk
from snake.Frames.Difficulty import Difficulty
from snake.Frames.StartPage import StartPage
# Buttons: Start Game
#          Difficulty level: Easy, Medium, Hard
#          Quit


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Snake")
        self.frames = dict()
        self.geometry("600x620")
        self.configure(background="black")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid()

        for FrameClass in (StartPage, Difficulty):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(StartPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


root = MainWindow()
root.mainloop()
