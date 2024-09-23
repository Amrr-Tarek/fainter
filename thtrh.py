import tkinter as tk
from tkinter import ttk


class KernelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kernel Grid")

        # Define a list for kernel values (initially empty)
        self.kernel_values = []

        # Set grid size (e.g., 5x5)
        self.grid_size = 5

        # Create a frame for the grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)

        # Create the grid of entry fields
        self.kernel_entries = []
        for i in range(self.grid_size):
            row_entries = []
            for j in range(self.grid_size):
                entry = tk.Entry(self.grid_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.kernel_entries.append(row_entries)

        # Button to insert values into the grid
        self.insert_button = tk.Button(
            self.root, text="Insert Values", command=self.insert_values
        )
        self.insert_button.pack(pady=10)

    def insert_values(self):
        # Define your kernel values here
        self.kernel_values = [
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            1,
            1,
            0,
            0,
            0,
            1,
            1,
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            1,
        ]

        # Insert values into the grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.kernel_entries[i][j].delete(0, tk.END)  # Clear existing value
                self.kernel_entries[i][j].insert(
                    0, self.kernel_values[i * self.grid_size + j]
                )


# Create the main window
root = tk.Tk()
app = KernelApp(root)
root.mainloop()
