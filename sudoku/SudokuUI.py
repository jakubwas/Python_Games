from sudoku.SudokuLogic import Sudoku
import tkinter as tk
from tkinter import ttk
import copy


class SudokuUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        # If width or height of the cell is changed, then width and height in canvas should be also changed
        self.CELL = 55
        self.geometry("{0}x{1}".format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.title("Sudoku")

        sudoku = Sudoku()
        self.random_board_original = sudoku.generate_random_sudoku()
        self.current_board = copy.deepcopy(self.random_board_original)
        sudoku.print_board()
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

        self.canvas = tk.Canvas(self.board_frame, width=550, height=550)
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        self.button_start_game = ttk.Button(self.button_frame)
        self.button_start_game.grid(row=0, column=0)

        self.bind("<Button-1>", self.on_click)
        self.bind("<Key>", self.key_pressed)

        self.draw_board()
        self.fill_board_with_numbers()

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
        print(event.widget)
        print(x, y)

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


sudokuUI = SudokuUI()
sudokuUI.mainloop()
