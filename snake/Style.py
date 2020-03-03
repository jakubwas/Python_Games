from tkinter import ttk

COLOUR_BUTTON_ACTIVE = "#58c77c"
COLOUR_BUTTON_PRESSED = "#44e378"


class Style:
    def __init__(self):
        # Style and theme
        # frame_style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="black")
        # button_style
        style.configure(
            "TButton",
            foreground="red",
            borderwidth=2,
            background="black",
            font=("Helvetica", 10, "bold", "italic"),
            width=35)
        style.map(
            "TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE)],
        )

