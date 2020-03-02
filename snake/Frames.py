from tkinter import ttk
import tkinter as tk
from pygame import mixer

from snake.Snake import Snake
from snake.Style import Style

# Buttons: Start Game
#          Difficulty level: Easy, Medium, Hard
#          Quit

# Default game speed:
SPEED = 75
# Default button padding
pad_y = (0, 10)


# Change game speed (Difficulty level)
def change_speed(speed):
    global SPEED
    SPEED = speed


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Background music (pygame)
        music = mixer.init()
        mixer.music.load("./assets/Californication.mp3")
        mixer.music.play(-1)

        # Main Window
        self.title("Snake")
        self.frames = dict()
        self.geometry("600x620")
        self.configure(background="black")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Main frame that contains: StartPage, Difficulty, GameFrame
        container = ttk.Frame(self)
        container.grid()

        # Top frame window
        for FrameClass in (StartPage, Difficulty, GameFrame):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(StartPage)

    # Show the given frame on the top of each other:
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


# Start Page with 3 buttons: Start Game, Difficulty, Quit
class StartPage(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        # Style
        style = Style()

        # Start game button
        button_start_game = ttk.Button(self, text="\nStart Game\n", command=lambda:
        controller.show_frame(GameFrame))

        button_start_game.grid(row=0, column=0, sticky="EW", pady=pad_y)

        # Difficulty button
        button_difficulty = ttk.Button(self, text="\nDifficulty level\n", command=lambda:
        controller.show_frame(Difficulty))

        button_difficulty.grid(row=1, column=0, sticky="EW", pady=pad_y)

        # Option button
        # button_option = ttk.Button(self, text="\nOption\n")

        # button_option.grid(row=2, column=0, sticky="EW", pady=pad_y)

        # Quit button
        button_quit = ttk.Button(self, text="\nQuit\n", command=quit)

        button_quit.grid(row=3, column=0, sticky="EW", pady=pad_y)


# Game Frame
class GameFrame(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        # Expand the frame if there is an extra space
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Label that shows up when the user press 'Start Game' button
        label = tk.Label(self,
                         text="Press 'a' to start",
                         foreground="red",
                         background="black",
                         font=("Helvetica", 18, "bold", "italic")
                         )
        label.grid(row=0, column=0, sticky="NSEW")
        self.bind_all("<Key>", self.on_key_press)

    # The game starts when the user press 'a'.
    def on_key_press(self, e):
        key = e.keysym
        if key == "a":
            snake_obj = Snake(SPEED, self.controller, StartPage)
            snake_obj.grid()


# Difficulty Frame
class Difficulty(ttk.Frame):
    def __init__(self, container, controller, speed=75):
        super().__init__(container)

        style = Style()

        # Difficulty level: easy, speed = 100
        button_easy = ttk.Button(self, text="\nEasy\n", command=lambda:
                                [controller.show_frame(GameFrame), change_speed(100)])
        button_easy.grid(row=1, column=0, pady=pad_y)

        # Difficulty level: medium, speed = 75
        button_medium = ttk.Button(self, text="\nMedium\n", command=lambda:
                                  [controller.show_frame(GameFrame), change_speed(75)])
        button_medium.grid(row=2, column=0, pady=pad_y)

        # Difficulty level: hard, speed = 50
        button_hard = ttk.Button(self, text="\nHard\n", command=lambda:
                                [controller.show_frame(GameFrame), change_speed(50)])
        button_hard.grid(row=3, column=0, pady=pad_y)


root = MainWindow()
root.mainloop()
