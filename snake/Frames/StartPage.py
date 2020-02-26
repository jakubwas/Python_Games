from tkinter import ttk
from snake.Frames.style import Style
from snake.Frames.Difficulty import Difficulty

COLOUR_BUTTON_ACTIVE = "#58c77c"
COLOUR_BUTTON_PRESSED = "#44e378"


class StartPage(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        pad_y = (0, 10)

        style = Style()

        # Start game button
        button_start_game = ttk.Button(self, text="\nStart Game\n")

        button_start_game.grid(row=0, column=0, sticky="EW", pady=pad_y)

        # Difficulty button
        button_difficulty = ttk.Button(self, text="\nDifficulty level\n", command=lambda:
                                       controller.show_frame(Difficulty))

        button_difficulty.grid(row=1, column=0, sticky="EW", pady=pad_y)

        # Option button
        button_option = ttk.Button(self, text="\nOption\n")

        button_option.grid(row=2, column=0, sticky="EW", pady=pad_y)

        # Quit button
        button_quit = ttk.Button(self, text="\nQuit\n", command=quit)

        button_quit.grid(row=3, column=0, sticky="EW", pady=pad_y)

