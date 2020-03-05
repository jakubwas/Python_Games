import random
import copy
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class Sudoku:

    def __init__(self):
        self.board = []
        self.solved_board = None
        self.new_board()

    def new_board(self):
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def print_board(self):
        print("—————————————————————————")
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("—————————————————————————")
            for j in range(9):
                if j % 3 == 0:
                    print("|", end=" ")
                if j == 8:
                    print(str(self.board[i][8]) + " |")
                else:
                    print(self.board[i][j], end=" ")
        print("—————————————————————————")

# SUDOKU SOLVER
    #  function used to find which positions are empty so that we could put a number there
    def is_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    #  coordinates = (row, column)
    #  function used to check if given position is valid ( there is two same numbers in a row, a column and in a box )
    def is_valid(self, number, coordinate):
        #  check if the row is valid
        for i in range(9):
            if self.board[coordinate[0]][i] == number and coordinate[1] != i:  # coordinate[1] != i is because we don't
                # want to check the row where we want to put a number
                return False

        #  check if the column is valid
        for i in range(9):
            if self.board[i][coordinate[1]] == number and coordinate[0] != i:
                return False

        #  check if the box is valid
        box_x_coordinate = coordinate[1] // 3  # we use integer division to define in which box we currently are
        box_y_coordinate = coordinate[0] // 3  # (0,1,2) // 3 = 0 | (3,4,5) // 3 = 1 | (6, 7, 8) // 3 = 2
        """
        -------------------------
        | (0,0) | (0,1) | (0,2) |
        -------------------------
        | (1,0) | (1,1) | (1,2) |
        -------------------------
        | (2,0) | (2,1) | (2,2) |
        -------------------------
        """
        for i in range(box_x_coordinate * 3, box_x_coordinate * 3 + 3):
            for j in range(box_y_coordinate * 3, box_y_coordinate * 3 + 3):
                if self.board[j][i] == number and (j, i) != coordinate:
                    return False
        return True  # we return False if at least one of upper conditions return False, otherwise we return True

    #  function which is used to solve sudoku, contains all upper method ( except the print_board method)
    def solve_board(self):
        empty_coordinates = self.is_empty()
        if not empty_coordinates:
            return True
        else:
            row, column = empty_coordinates
        for i in range(1, 10):
            if self.is_valid(i, (row, column)):
                self.board[row][column] = i
                if self.solve_board():
                    return True
                else:
                    self.board[row][column] = 0
        return False

    def generate_random_full_board(self):
        empty_coordinates = self.is_empty()
        if not empty_coordinates:
            return True
        else:
            row, column = empty_coordinates

        random.shuffle(valid_numbers)

        for number in valid_numbers:
            if self.is_valid(number, (row, column)):
                self.board[row][column] = number
                if self.generate_random_full_board():
                    return True
                else:
                    self.board[row][column] = 0

    def generate_random_sudoku(self):
        self.generate_random_full_board()
        self.solved_board = copy.deepcopy(self.board)
        how_many_numbers = random.randint(60, 65)
        print(how_many_numbers)
        sequence = [i for i in range(81)]
        cords = set()
        while len(cords) != how_many_numbers:
            cords.add(random.choice(sequence))
        cords = list(cords)
        for i in range(how_many_numbers):
            row = cords[i] // 9
            col = cords[i] % 9
            self.board[row][col] = 0
        return self.board

