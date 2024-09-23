import tkinter as tk
from tkinter import ttk


def change_color(color):
    """Change the background color of the window."""
    new_window.config(bg=color)


def open_new_window():
    """Create a new window with radio buttons in the menu bar."""
    global new_window
    new_window = tk.Toplevel(root)
    new_window.title("Color Selector")

    # Create a menu bar
    menu_bar = tk.Menu(new_window)
    new_window.config(menu=menu_bar)

    # Create a "Colors" menu
    colors_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Colors", menu=colors_menu)

    # Add radio buttons to the menu
    colors_menu.add_radiobutton(
        label="Red",
        variable=color_var,
        value="red",
        command=lambda: change_color("red"),
    )
    colors_menu.add_radiobutton(
        label="Green",
        variable=color_var,
        value="green",
        command=lambda: change_color("green"),
    )
    colors_menu.add_radiobutton(
        label="Blue",
        variable=color_var,
        value="blue",
        command=lambda: change_color("blue"),
    )

    # Set default color
    color_var.set("red")  # Default to red
    change_color(color_var.get())  # Apply default color


root = tk.Tk()
root.title("Main Window")

# Variable to track selected color
color_var = tk.StringVar()

# Button to open the new window
open_button = tk.Button(root, text="Open Color Selector", command=open_new_window)
open_button.pack(pady=20)

root.mainloop()
