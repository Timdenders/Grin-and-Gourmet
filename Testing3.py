import tkinter as tk
from tkinter import messagebox


class Image:
    def __init__(self, imagePath):
        self.imagePath = imagePath

    def getImagePath(self):
        return self.imagePath

    def setImagePath(self, imagePath):
        self.imagePath = imagePath


class Recipe:
    def __init__(self, name, instructions, images=None, rating=0):
        self.name = name
        self.instructions = instructions
        self.images = images if images else []
        self.rating = rating

    def getName(self):
        return self.name

    def getInstructions(self):
        return self.instructions

    def getImages(self):
        return self.images

    def getRating(self):
        return self.rating

    def setName(self, name):
        self.name = name

    def setInstructions(self, instructions):
        self.instructions = instructions

    def setImages(self, images):
        self.images = images

    def setRating(self, rating):
        self.rating = rating


class RecipeManager:
    def __init__(self):
        self.recipes = []

    def addRecipe(self, recipe):
        self.recipes.append(recipe)

    def removeRecipe(self, recipe):
        if recipe in self.recipes:
            self.recipes.remove(recipe)
        else:
            print("Recipe not found.")

    def getRecipeByName(self, name):
        for recipe in self.recipes:
            if recipe.getName() == name:
                return recipe
        return None

    def filterRecipesByKeyword(self, keyword):
        filtered_recipes = []
        for recipe in self.recipes:
            if keyword.lower() in recipe.getName().lower():
                filtered_recipes.append(recipe)
        return filtered_recipes


class CookingAssistant:
    def __init__(self):
        self.recipes = RecipeManager()

    def displayRecipe(self, name):
        recipe = self.recipes.getRecipeByName(name)
        if recipe:
            info = f"Recipe Name: {recipe.getName()}\nInstructions: {recipe.getInstructions()}\nImages: {[image.getImagePath() for image in recipe.getImages()]}\nRating: {recipe.getRating()}"
            messagebox.showinfo("Recipe Details", info)
        else:
            messagebox.showerror("Error", "Recipe not found.")

    def filterRecipes(self, keyword):
        filtered_recipes = self.recipes.filterRecipesByKeyword(keyword)
        if filtered_recipes:
            recipes_list = ', '.join([recipe.getName() for recipe in filtered_recipes])
            messagebox.showinfo("Filtered Recipes", f"Recipes containing '{keyword}': {recipes_list}")
        else:
            messagebox.showinfo("Filtered Recipes", f"No recipes found for the given keyword.")


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

        # Creating an instance of CookingAssistant to handle actions
        self.cooking_assistant = CookingAssistant()

    def display_recipe(self):
        recipe_name = self.entry.get()
        self.cooking_assistant.displayRecipe(recipe_name)

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