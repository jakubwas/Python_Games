from sudoku.SudokuLogic import Sudoku
import tkinter as tk
from tkinter import ttk
import copy
import time

COLOUR_BUTTON_NORMAL = "#5fba7d"
COLOUR_BUTTON_ACTIVE = "#58c77c"
COLOUR_BUTTON_PRESSED = "#44e378"


class SudokuUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.WINDOW_WIDTH = 824
        self.WINDOW_HEIGHT = 600
        # If width or height of the cell is changed, then width and height in canvas should be also changed
        self.CELL = 55
        self.resizable(False, False)
        self.geometry("{0}x{1}".format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.title("Sudoku")
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

        self.sudoku = Sudoku()
        self.random_board_original = self.sudoku.generate_random_sudoku()
        self.current_board = copy.deepcopy(self.random_board_original)
        self.sudoku.print_board()
        self.solution = None
        self.row = -1
        self.col = -1

        # Main Frame
        self.container = tk.Frame(self, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        self.container.grid(row=0, column=0, sticky="NSEW")

        self.board_frame = tk.Frame(self.container)
        self.board_frame.grid(row=0, column=0, sticky="NSEW")

        self.button_frame = tk.Frame(self.container)
        self.button_frame.grid(row=0, column=1, sticky="NSEW")
        self.button_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.board_frame, width=550, height=550)
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        # Buttons
        style = ttk.Style()
        style.configure(
            "TButton",
            font=("Helvetica", 15, "italic"),
            width=18,
            borderwidth=0,
            background=COLOUR_BUTTON_NORMAL)
        style.map(
            "SendButton.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE)],
        )

        self.button_start_game = ttk.Button(self.button_frame, text="Start new Game", command=self.start_new_game)
        self.button_start_game.grid(row=0, column=0, pady=(60, 0), padx=(35, 35))

        self.button_reset_current_board = ttk.Button(self.button_frame, text="Reset current Board")
        self.button_reset_current_board.grid(row=1, column=0, pady=(30, 0), padx=(35, 35))

        self.button_show_hint = ttk.Button(self.button_frame, text="Show hint")
        self.button_show_hint.grid(row=2, column=0, pady=(30, 0), padx=(35, 35))

        self.button_solve = ttk.Button(self.button_frame, text="Show solution")
        self.button_solve.grid(row=3, column=0, pady=(30, 0), padx=(35, 35))

        self.button_about = ttk.Button(self.button_frame, text="About")
        self.button_about.grid(row=4, column=0, pady=(30, 0), padx=(35, 35))

        self.label_time = ttk.Label(self.button_frame, text="Your time")
        self.label_time.grid(row=5, column=0, pady=(10, 0))

        self.text_variable = tk.StringVar(value="00:00")
        self.label_timer = ttk.Label(self.button_frame, textvariable=self.text_variable, style="timer.TLabel")
        style.configure(
            "timer.TLabel",
            font=("Helvetica", 22, "italic")
        )

        self.label_timer.grid(row=6, column=0)

        self.button_quit = ttk.Button(self.button_frame, text="Quit")
        self.button_quit.grid(row=7, column=0, pady=(30, 0), padx=(35, 35))

        self.bind("<Button-1>", self.on_click)
        self.bind("<Key>", self.key_pressed)

        self.draw_board()
        self.fill_board_with_numbers()
        self.update_time()

    def draw_board(self):
        for i in range(1, 11):
            if (i - 1) % 3 == 0:
                color = "blue"
            else:
                color = "black"

            line_width = 2.2 if i == 1 or i == 10 else 1

            # Horizontal lines
            x0 = self.CELL
            y0 = i * self.CELL
            x1 = self.CELL * 10
            y1 = i * self.CELL
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=line_width)
            # Vertical lines
            x0 = i * self.CELL
            y0 = self.CELL
            x1 = i * self.CELL
            y1 = self.CELL * 10
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=line_width)

    def fill_board_with_numbers(self):
        for i in range(9):
            for j in range(9):
                if self.current_board[i][j] != 0:
                    x = self.CELL + j * self.CELL + self.CELL / 2
                    y = self.CELL + i * self.CELL + self.CELL / 2
                    if self.random_board_original[i][j]:
                        color = "black"
                        font = ("Helvetica", 14, "bold")
                    else:
                        color = "grey"
                        font = ("Helvetica", 12)
                    self.canvas.create_text(x, y, text=self.current_board[i][j], tags="numbers", font=font, fill=color)

    def on_click(self, event):
        x, y = event.x, event.y
        if str(event.widget) != ".!frame.!frame.!canvas":
            return

        if (self.CELL <= x <= self.CELL * 10) and (self.CELL <= y <= self.CELL * 10):
            row = int((y - self.CELL) / self.CELL)
            col = int((x - self.CELL) / self.CELL)
            print(row, col)
            if (0 <= (row and col) <= 8) and self.random_board_original[row][col] == 0:
                # Delete red_border after next time we click the cell if it's currently chosen
                if row == self.row and col == self.col:
                    self.row = -1
                    self.col = -1
                    self.canvas.delete("red_border")
                    return

                self.row = row
                self.col = col

                self.canvas.delete("red_border")
                x0 = self.CELL + self.CELL * self.col
                y0 = self.CELL + self.CELL * self.row
                x1 = 2 * self.CELL + self.CELL * self.col
                y1 = 2 * self.CELL + self.CELL * self.row
                self.canvas.create_rectangle((x0, y0, x1, y1), outline="red", tag="red_border", width=1.5)
            else:
                self.row = -1
                self.col = -1

    def key_pressed(self, event):
        key = event.keysym
        if str(key) in "123456789" and (self.row and self.col) != -1:
            self.current_board[self.row][self.col] = int(key)
            self.canvas.delete("numbers")
            self.fill_board_with_numbers()
        elif key == "BackSpace":
            self.current_board[self.row][self.col] = 0
            self.canvas.delete("numbers")
            self.fill_board_with_numbers()

    def update_time(self):
        # The time is displayed in format -> hours:minutes:seconds
        # Seconds
        if self.seconds < 10:
            seconds = "0"+str(self.seconds)
        else:
            seconds = str(self.seconds)
        # Minutes
        if self.minutes < 10:
            minutes = "0" + str(self.minutes)
        else:
            minutes = str(self.minutes)
        # Hours (hours are displayed when they are > 0)
        if self.hours == 0:
            hours = ""
        else:
            hours = "0" + str(self.hours) + ":"

        # When this variable is updated, the label_timer text is change
        self.text_variable.set(hours+minutes+":"+seconds)
        # Update seconds, minutes and hours
        if self.seconds == 59:
            self.minutes += 1
            self.seconds = -1
        if self.seconds == 59 and self.minutes == 59:
            self.seconds = -1
            self.minutes = 0
            self.hours = 1

        self.seconds += 1
        # After 1 s call update_time method
        self.after(1000, self.update_time)

    def reset_time(self):
        self.seconds = 0
        self.minutes = 0

    def start_new_game(self):
        self.reset_time()



sudokuUI = SudokuUI()
sudokuUI.mainloop()
