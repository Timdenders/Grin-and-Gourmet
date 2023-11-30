import tkinter as tk
from tkinter import messagebox
from RecipeManager import *
from PIL import Image, ImageTk

class CookingAssistant:
    def __init__(self):
        self.recipes = RecipeManager()
        self.loaded = False

    def loadRecipes(self, file_name):
        if not self.loaded:
            self.recipes.loadRecipesFromCSV(file_name)
            self.loaded = True

    def getRecipeNames(self):
        self.loadRecipes("recipes.csv")
        recipe_names = [recipe.getName() for recipe in self.recipes.recipes]
        recipe_names.sort()
        recipe_names.insert(0, "Select Recipe")
        return recipe_names

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

        # Dropdown for recipe selection
        self.selected_recipe = tk.StringVar(master)
        self.dropdown = tk.OptionMenu(master, self.selected_recipe, *self.get_recipe_names())
        self.dropdown.grid(row=0, column=0, padx=5, pady=5)  # Placed in the first row and column

        self.selected_recipe.set(self.get_recipe_names()[0])

        self.display_button = tk.Button(master, text="Display Recipe", command=self.display_recipe)
        self.display_button.grid(row=0, column=1, padx=5, pady=5)  # Placed in the first row and second column

        self.filter_label = tk.Label(master, text="Enter Keyword to Filter Recipes:")
        self.filter_label.grid(row=1, column=0, padx=5, pady=5)  # Placed in the second row and first column

        self.filter_entry = tk.Entry(master)
        self.filter_entry.grid(row=1, column=1, padx=5, pady=5)  # Placed in the second row and second column

        self.filter_button = tk.Button(master, text="Filter Recipes", command=self.filter_recipes)
        self.filter_button.grid(row=2, columnspan=2, padx=5, pady=5)  # Spans across two columns in the third row

    def display_recipe(self):
        selected_recipe = self.selected_recipe.get()

        if selected_recipe.lower() == "Select Recipe".lower():
            messagebox.showerror("Error", "Please select a recipe.")
        else:
            self.cooking_assistant.loadRecipes("recipes.csv")
            recipe = self.cooking_assistant.recipes.getRecipeByName(selected_recipe)
            if recipe:
                recipe_window = tk.Toplevel(self.master)
                recipe_window.title(selected_recipe)

                recipe_frame = tk.Frame(recipe_window)
                recipe_frame.pack()

                # Recipe Name
                name_label = tk.Label(recipe_frame, text=f"{recipe.getName()}")
                name_label.pack()

                # Images
                images = recipe.getImages()
                for i, image in enumerate(images):
                    if image.getImagePath():
                        try:
                            img = Image.open(image.getImagePath())
                            img = img.resize((200, 200))  # Resize the image as needed
                            photo = ImageTk.PhotoImage(img)
                            image_label = tk.Label(recipe_frame, image=photo)
                            image_label.image = photo
                            image_label.pack()

                        except FileNotFoundError:
                            error_label = tk.Label(recipe_frame, text="Image not found")
                            error_label.pack()
                    else:
                        error_label = tk.Label(recipe_frame, text="No image path provided")
                        error_label.pack()

                # Rating
                rating_label = tk.Label(recipe_frame, text=f"Rating: {recipe.getRating()}")
                rating_label.pack()

                # Ingredients
                ingredients_label = tk.Label(recipe_frame, text="Ingredients:")
                ingredients_label.pack()
                ingredients_text = tk.Text(recipe_frame, wrap="word", height=10, width=50)
                ingredients_text.insert(tk.END, recipe.getIngredients())
                ingredients_text.config(state=tk.DISABLED)
                ingredients_text.pack()

                # Instructions
                instructions_label = tk.Label(recipe_frame, text="Instructions:")
                instructions_label.pack()
                instructions_text = tk.Text(recipe_frame, wrap="word", height=15, width=50)
                instructions_text.insert(tk.END, recipe.getInstructions())
                instructions_text.config(state=tk.DISABLED)
                instructions_text.pack()

            else:
                messagebox.showerror("Error", "Recipe not found.")

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
