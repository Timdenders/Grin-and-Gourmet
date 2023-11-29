import tkinter as tk
from tkinter import messagebox
from RecipeManager import *


class CookingAssistant:
    def __init__(self):
        self.recipes = RecipeManager()

    def displayRecipe(self, selected_recipe):
        self.recipes.loadRecipesFromCSV("recipes.csv")
        recipe = self.recipes.getRecipeByName(selected_recipe.get())
        if recipe:
            info = (f"Recipe Name: {recipe.getName()}\n"
                    f"Ingredients: {recipe.getIngredients()}"
                    f"Instructions: {recipe.getInstructions()}\n"
                    f"Images: {[image.getImagePath() for image in recipe.getImages()]}\n"
                    f"Rating: {recipe.getRating()}")
            messagebox.showinfo("Recipe Details", info)
        else:
            messagebox.showerror("Error", "Recipe not found.")

    def getRecipeNames(self):
        self.recipes.loadRecipesFromCSV("recipes.csv")
        return [recipe.getName() for recipe in self.recipes.recipes]

    def filterRecipes(self, keyword):
        filtered_recipes = self.recipes.filterRecipesByKeyword(keyword)
        if filtered_recipes:
            recipes_list = ', '.join([recipe.getName() for recipe in filtered_recipes])
            messagebox.showinfo("Filtered Recipes", f"Recipes containing '{keyword}': {recipes_list}")
        else:
            messagebox.showinfo("Filtered Recipes", f"No recipes found for the given keyword.")


class CookingAssistantGUI:
    def __init__(self, master):
        # Creating an instance of CookingAssistant to handle actions
        self.cooking_assistant = CookingAssistant()

        self.master = master
        self.master.title("Cooking Assistant")

        # Creating widgets
        self.label = tk.Label(master, text="Select Recipe:")
        self.label.pack()

        # Dropdown for recipe selection
        self.selected_recipe = tk.StringVar(master)
        self.dropdown = tk.OptionMenu(master, self.selected_recipe, *self.get_recipe_names())
        self.dropdown.pack()

        self.display_button = tk.Button(master, text="Display Recipe", command=self.display_recipe)
        self.display_button.pack()

        self.filter_label = tk.Label(master, text="Enter Keyword to Filter Recipes:")
        self.filter_label.pack()

        self.filter_entry = tk.Entry(master)
        self.filter_entry.pack()

        self.filter_button = tk.Button(master, text="Filter Recipes", command=self.filter_recipes)
        self.filter_button.pack()

    def display_recipe(self):
        self.cooking_assistant.displayRecipe(self.selected_recipe)

    def get_recipe_names(self):
        return self.cooking_assistant.getRecipeNames()

    def filter_recipes(self):
        keyword = self.filter_entry.get()
        self.cooking_assistant.filterRecipes(keyword)


def run_gui():
    root = tk.Tk()
    app = CookingAssistantGUI(root)
    root.mainloop()


# Running the GUI
if __name__ == "__main__":
    run_gui()
