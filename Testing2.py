import tkinter as tk
from tkinter import messagebox


class CookingAssistantGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Cooking Assistant")

        # Creating widgets
        self.label = tk.Label(master, text="Enter Recipe Name:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.display_button = tk.Button(master, text="Display Recipe", command=self.display_recipe)
        self.display_button.pack()

        self.filter_label = tk.Label(master, text="Enter Keyword to Filter Recipes:")
        self.filter_label.pack()

        self.filter_entry = tk.Entry(master)
        self.filter_entry.pack()

        self.filter_button = tk.Button(master, text="Filter Recipes", command=self.filter_recipes)
        self.filter_button.pack()

    def display_recipe(self):
        recipe_name = self.entry.get()
        # Fetch recipe information based on name and display it in a messagebox or in a separate section of the GUI
        messagebox.showinfo("Recipe Display", f"Displaying recipe for: {recipe_name}")

    def filter_recipes(self):
        keyword = self.filter_entry.get()
        # Fetch recipes based on keyword and display them in a list or messagebox
        messagebox.showinfo("Filtered Recipes", f"Recipes containing '{keyword}': [Recipe1, Recipe2, ...]")


def run_gui():
    root = tk.Tk()
    app = CookingAssistantGUI(root)
    root.mainloop()


# Running the GUI
if __name__ == "__main__":
    run_gui()
