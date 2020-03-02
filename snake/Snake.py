import tkinter as tk
from PIL import ImageTk, Image
from random import randint


class Snake(tk.Canvas):
    def __init__(self, speed, controller, start_page):
        super().__init__(highlightthickness=0, width=600, height=620, background="black")

        self.controller = controller
        self.start_page = start_page
        # Default speed is 75
        self.speed = speed
        # Beginning score
        self.score = 0
        # Start snake position
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        # Beginning food position
        self.food_position = [(200, 200)]
        # At the beginning snake moves to the right
        self.direction = "Right"
        # Snake's image has 20px
        self.MOVE = 20

        self.load_images()
        self.bind_all("<Key>", self.on_key_press)
        self.after(self.speed, self.perform_action)

    # Load images and put them on the screen
    def load_images(self):
        # create text with score
        self.create_text(
            35, 12, text=f"     Score: {self.score}", tag="score", fill="#fff", font=10
        )
        # Load images if the path is correct, otherwise destroy the root
        try:
            snake_body_image = Image.open("assets/snake.png")
            self.snake_image = ImageTk.PhotoImage(snake_body_image)
            food_image_x = Image.open("assets/food.png")
            self.food_image = ImageTk.PhotoImage(food_image_x)
        except IOError:
            print("There is no images to load !!!")
        # If images were loaded, put them on the screen
        # snake_images
        for position in self.snake_positions:
            self.create_image(*position, image=self.snake_image, tag="snake")
        # food_image
        self.create_image(*self.food_position, image=self.food_image, tag="food")
        # create rectangle which initialize the board game
        self.create_rectangle(7, 27, 593, 613, outline="#0019bf")

    # How does the snake move ?
    def move_snake(self):
        # Coordinates of the snake's head
        head_x_position, head_y_position = self.snake_positions[0]
        # Snake's image has 20px. Depends on what direction the user choose, add or subtract 20px from snake's head
        # position so that we now have new coordinates of the snake's head. Then update the snake_position so that now
        # it contains new head coordinates and old elements except the last one.
        # Update snake's coordinates
        if self.direction == "Right":
            new_head_position = [(head_x_position + self.MOVE, head_y_position)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]
        if self.direction == "Left":
            new_head_position = [(head_x_position - self.MOVE, head_y_position)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]
        if self.direction == "Up":
            new_head_position = [(head_x_position, head_y_position - self.MOVE)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]
        if self.direction == "Down":
            new_head_position = [(head_x_position, head_y_position + self.MOVE)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]
        # Change the location of the snake's images to the new one.
        for i, j in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(i, *j)

    # Define when the game ends
    def check_collision(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (
                head_x_position in (0, 600)
                or head_y_position in (20, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position[0]:
            self.score += 1
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"     Score: {self.score}", tag="score")
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_image, tag="snake")
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position[0])

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * self.MOVE
            y_position = randint(3, 30) * self.MOVE
            food_position = (x_position, y_position)
            if food_position not in self.snake_positions:
                return [food_position]

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = {"Right", "Left", "Up", "Down"}
        opposite_directions = ({"Right", "Left"}, {"Up", "Down"})

        if (
                new_direction in all_directions
                and {new_direction, self.direction} not in opposite_directions
        ):
            self.direction = new_direction

    def play_again(self, e):
        key = e.keysym
        if key == "a":
            self.destroy()
            snake = Snake(self.speed, self.controller, self.start_page)
            snake.grid()
        elif key == "Escape":
            self.controller.show_frame(self.start_page)
            self.destroy()

    def perform_action(self):
        if self.check_collision():
            self.delete(tk.ALL)
            self.create_text(
                self.winfo_width() / 2,
                self.winfo_height() / 2,
                text=f"    Game over! You scored {self.score}!\n        Press 'a' to play again\nor escape to go to main menu.",
                fill="#fff",
                font=15
            )
            self.bind_all("<Key>", self.play_again)
        self.check_food_collision()
        self.move_snake()
        self.after(self.speed, self.perform_action)
