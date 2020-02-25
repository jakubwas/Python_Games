import tkinter as tk
from PIL import ImageTk, Image
from random import randint

MOVE = 20


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black")
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = [(200, 200)]
        self.direction = "Right"
        self.load_images()
        self.bind_all("<Key>", self.on_key_press)
        self.after(75, self.perform_action)

    def load_images(self):
        # Load images if the path is correct, otherwise destroy root
        try:
            snake_body_image = Image.open("./assets/snake.png")
            self.snake_image = ImageTk.PhotoImage(snake_body_image)

            food_image_x = Image.open("./assets/food.png")
            self.food_image = ImageTk.PhotoImage(food_image_x)
        except IOError:
            print("There is no images to load !!!")
            root.destroy()
        # If images were loaded, put them on the screen
        # snake_images
        for position in self.snake_positions:
            self.create_image(*position, image=self.snake_image, tag="snake")
        self.create_image(*self.food_position, image=self.food_image, tag="food")

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]
        if self.direction == "Right":
            new_head_position = [(head_x_position + MOVE, head_y_position)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]
        if self.direction == "Left":
            new_head_position = [(head_x_position - MOVE, head_y_position)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]
        if self.direction == "Up":
            new_head_position = [(head_x_position, head_y_position - MOVE)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]
        if self.direction == "Down":
            new_head_position = [(head_x_position, head_y_position + MOVE)]
            self.snake_positions = new_head_position + self.snake_positions[:-1]

        for i, j in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(i, *j)

    def check_collision(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (
                head_x_position in (0, 600)
                or head_y_position in (0, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:]
                )

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position[0]:
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_image, tag="snake")
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position[0])

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE
            y_position = randint(3, 30) * MOVE
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

    def perform_action(self):
        if self.check_collision():
            self.delete(tk.ALL)
        self.check_food_collision()
        self.move_snake()
        self.after(75, self.perform_action)


root = tk.Tk()
snake = Snake()
snake.pack()
root.mainloop()
