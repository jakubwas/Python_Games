from sudoku.SudokuLogic import Sudoku
import tkinter as tk
from tkinter import ttk
import copy

# Button style color
COLOUR_BUTTON_NORMAL = "#5fba7d"
COLOUR_BUTTON_ACTIVE = "#58c77c"
COLOUR_BUTTON_PRESSED = "#44e378"

# Difficulty levels; 81 - level = amount of numbers that the board has
EASY = 40
MEDIUM = 50
HARD = 55


class SudokuUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # Size of main root window
        self.WINDOW_WIDTH = 830
        self.WINDOW_HEIGHT = 600
        self.geometry("{0}x{1}".format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # Width/Height of the single cell
        self.CELL = 55
        # The size of main window can't be changed
        self.resizable(False, False)
        # Title
        self.title("Sudoku")
        # Seconds, minutes and hours (label_time)
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        # Variables that indicate current row and column. If coordinates of the cursor are not pointing to any cell,
        # then the value = -1
        self.row = -1
        self.col = -1
        # When the stop_the_clock is True, then the clock stops
        self.stop_the_clock = None
        # Make sure we don't call after method many times at the same time
        self.multiple_after_methods = None

        #                                           Frames/canvas
        # Main frame
        self.container = tk.Frame(self, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        self.container.grid(row=0, column=0, sticky="NSEW")
        # Button frame
        self.button_frame = tk.Frame(self.container)
        self.button_frame.grid(row=0, column=1, sticky="NSEW")
        self.button_frame.columnconfigure(0, weight=1)
        # Difficulty level frame
        self.difficulty_frame = tk.Frame(self.button_frame)
        self.difficulty_frame.grid(row=8, column=0, sticky="NSEW", pady=(10, 0), padx=(50, 0))
        # Canvas (which includes sudoku grid)
        self.canvas = tk.Canvas(self.container, width=550, height=550)
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        #                                             Widget's style
        style = ttk.Style()
        # All buttons have the same style
        style.configure(
            "TButton",
            font=("Helvetica", 15, "italic"),
            width=19,
            borderwidth=0,
            background=COLOUR_BUTTON_NORMAL)
        style.map(
            "TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE)],
        )
        # Timer style
        style.configure(
            "timer.TLabel",
            font=("Helvetica", 22, "italic")
        )
        #                                             Buttons
        # Start Game button
        self.button_start_game = ttk.Button(self.button_frame, text="Start new Game", command=self.start_new_game)
        self.button_start_game.grid(row=0, column=0, pady=(70, 0), padx=(35, 35), ipady=5)
        # Reset game button
        self.button_reset_current_board = ttk.Button(self.button_frame, text="Reset current Board",
                                                     command=self.reset_current_board)
        self.button_reset_current_board.grid(row=1, column=0, pady=(30, 0), padx=(35, 35))
        # Check button
        self.button_check = ttk.Button(self.button_frame, text="Check current answers",
                                       command=self.check_current_answers)
        self.button_check.grid(row=2, column=0, pady=(30, 0), padx=(35, 35))
        # Show solution button
        self.button_solve = ttk.Button(self.button_frame, text="Show solution", command=self.show_solution)
        self.button_solve.grid(row=3, column=0, pady=(30, 0), padx=(35, 35))
        # Quit button
        self.button_quit = ttk.Button(self.button_frame, text="Quit", command=self.destroy)
        self.button_quit.grid(row=9, column=0, pady=(30, 0), padx=(35, 35))

        #                                         Labels
        # Your time label
        self.label_time = ttk.Label(self.button_frame, text="Your time")
        self.label_time.grid(row=5, column=0, pady=(10, 0))
        # Every time the text_variable change, the label_timer's text updates
        self.text_variable = tk.StringVar(value="00:00")
        self.label_timer = ttk.Label(self.button_frame, textvariable=self.text_variable, style="timer.TLabel")
        self.label_timer.grid(row=6, column=0)
        # Difficulty level
        self.label_difficulty = ttk.Label(self.button_frame, text="Difficulty level")
        self.label_difficulty.grid(row=7, column=0, pady=(20, 0))

        #                                      RadioButtons
        #
        self.level = tk.IntVar()
        # Easy
        self.radiobutton_easy = ttk.Radiobutton(
            self.difficulty_frame,
            text="Easy",
            variable=self.level,
            value=EASY)
        self.radiobutton_easy.grid(row=0, column=0)
        # Medium
        self.radiobutton_medium = ttk.Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.level,
            value=MEDIUM)
        self.level.set(MEDIUM)  # Default difficulty level is medium
        self.radiobutton_medium.grid(row=0, column=1)
        # Hard
        self.radiobutton_hard = ttk.Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.level,
            value=HARD)
        self.radiobutton_hard.grid(row=0, column=2)

        # Initialize boards
        self.sudoku = Sudoku()  # Sudoku logic
        self.random_board_original = None  # Original board generated with SudokuLogic
        self.current_board = None  # Current board where we put user input
        self.solution = None  # Original board with solution

        # Draw sudoku grid, put the numbers there and start the game.
        self.draw_board()
        self.start_new_game()

    # Events
    def bind_(self):
        self.bind("<Button-1>", self.on_click)  # Left click (select/deselect cell)
        self.bind("<Button-3>", self.on_click)  # Right click (delete content of the cell (if possible))
        self.bind("<Key>", self.key_pressed)  # Keyboard

    def unbind_(self):
        self.unbind("<Button-1>")
        self.unbind("<Button-3>")
        self.unbind("<Key>")

    # Delete all items with tags: numbers, red_border
    def delete_with_tags(self):
        self.canvas.delete("numbers")
        self.canvas.delete("red_border")

    # This method can be used to remove number from the cell or put the new one.
    def update_content_of_the_current_cell(self, row, col, value):  # if value = 0 then we remove element from the board
        self.current_board[row][col] = value
        self.canvas.delete("numbers")
        self.fill_board_with_numbers()

    # Reset current time (start again from 00:00)
    def reset_time(self):
        self.seconds = 0
        self.minutes = 0

    # Make sure we don't call after method many times at the same time
    def check_multi_after_methods(self):
        if self.multiple_after_methods:
            self.after_cancel(self.multiple_after_methods)
            self.multiple_after_methods = None
        self.update_time()

    # Draw grid (straight lines, without numbers)
    # This method is called only one time during the program.
    def draw_board(self):
        for i in range(1, 11):
            if (i - 1) % 3 == 0:
                color = "blue"
                line_width = 1.5
            else:
                color = "black"
                line_width = 1
            if i == 1 or i == 10:
                line_width = 2.2
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

    # Put the numbers from current_board to the board
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

    # We call this method when the user clicks on the cell with a single left/right-click of the mouse
    def on_click(self, event):
        # The x and y coordinates of where exactly the user clicked
        x, y = event.x, event.y
        # If x, y are not indicate to any cell, then quit
        if str(event.widget) != ".!frame.!canvas":
            return
        if (self.CELL <= x <= self.CELL * 10) and (self.CELL <= y <= self.CELL * 10):
            row = int((y - self.CELL) / self.CELL)
            col = int((x - self.CELL) / self.CELL)
            if (0 <= (row and col) <= 8) and self.random_board_original[row][col] == 0:
                # If we right-click on the cell, delete it's content
                if event.num == 3:
                    self.update_content_of_the_current_cell(row, col, 0)
                    return
                # If the cell had already been selected, then we’ll deselect the cell
                if row == self.row and col == self.col:
                    self.row = -1
                    self.col = -1
                    self.canvas.delete("red_border")
                    return  # Exit

                # Position of the current selected cell
                self.row = row
                self.col = col

                # Highlight the cell that the user has clicked on.
                self.canvas.delete("red_border")
                x0 = self.CELL + self.CELL * self.col
                y0 = self.CELL + self.CELL * self.row
                x1 = 2 * self.CELL + self.CELL * self.col
                y1 = 2 * self.CELL + self.CELL * self.row
                self.canvas.create_rectangle((x0, y0, x1, y1), outline="red", tag="red_border", width=1.5)
            # If we click on the cell which content can't be changed
            else:
                self.row = -1
                self.col = -1

    # Get the user input(number) when the cell is selected
    def key_pressed(self, event):
        key = event.keysym
        if str(key) in "123456789" and (self.row and self.col) != -1:
            self.update_content_of_the_current_cell(self.row, self.col, int(key))
        elif key == "BackSpace":
            self.update_content_of_the_current_cell(self.row, self.col, 0)

    # Update current time
    def update_time(self):
        # The time is displayed in format -> hours:minutes:seconds
        if self.stop_the_clock:
            return
        # Seconds
        if self.seconds < 10:
            seconds = "0" + str(self.seconds)
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
        self.text_variable.set(hours + minutes + ":" + seconds)
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
        self.multiple_after_methods = self.after(1000, self.update_time)

    # Start new game -> reset time, remove current board and display new one
    def start_new_game(self):
        self.start_reset_similarities()
        # Generate new board and remove old elements from grid
        self.sudoku.new_board()
        self.random_board_original = self.sudoku.generate_random_sudoku(int(self.level.get()))
        self.solution = self.sudoku.solved_board
        self.current_board = copy.deepcopy(self.random_board_original)
        self.fill_board_with_numbers()

    # Display the content of the random_board_original
    def reset_current_board(self):
        self.current_board = copy.deepcopy(self.random_board_original)
        self.start_reset_similarities()
        self.fill_board_with_numbers()

    # Method which combine similarities from start_new_game() and reset_current_board()
    def start_reset_similarities(self):
        self.delete_with_tags()
        # Bind again in case we click show_solution button where we unbind events.
        self.bind_()
        # If we call reset_current_board() or start_new_game() we want to reset the time
        self.reset_time()
        # Set the value of the stop_the_clock to False so that the update_time() could work
        self.stop_the_clock = False
        # Make sure we don't call after method many times at the same time
        self.check_multi_after_methods()

    # Check the current answers
    def check_current_answers(self):
        self.delete_with_tags()
        for i in range(9):
            for j in range(9):
                if self.current_board[i][j]:
                    # If the answer is correct:
                    if self.current_board[i][j] == self.solution[i][j]:
                        color = "black"
                    # If the answer is wrong
                    else:
                        color = "red"
                    self.check_show_similarities(i, j, color)

    # Show solution of the current board
    def show_solution(self):
        self.canvas.delete("numbers")
        self.canvas.delete("red_border")
        # When the solution pops up, the user can't put any data into grid (remove events)
        self.unbind_()
        # Stop updating the time when the solution is visible
        self.stop_the_clock = True
        for i in range(9):
            for j in range(9):
                if self.current_board[i][j] == self.solution[i][j] or self.current_board[i][j] == 0:
                    color = "black"
                else:
                    # Use red font color if the answer is incorrect
                    color = "red"
                self.check_show_similarities(i, j, color)

    # Method which combine similarities from check_current_answer() and show_solution()
    def check_show_similarities(self, i, j, color):
        font = ("Helvetica", 14, "bold")
        x = self.CELL + j * self.CELL + self.CELL / 2
        y = self.CELL + i * self.CELL + self.CELL / 2
        self.canvas.create_text(x, y, text=self.solution[i][j], tags="numbers", font=font, fill=color)


sudokuUI = SudokuUI()
sudokuUI.mainloop()
