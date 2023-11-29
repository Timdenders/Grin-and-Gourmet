from RecipeManager import *

if __name__ == "__main__":
    # Creating a Cooking Assistant instance
    cooking_assistant = CookingAssistant()

    # # Creating a few recipes
    # recipe1 = Recipe("Pasta", "Pasta","Boil pasta, add sauce.",  [Image("pasta_image.jpg")], 4)
    # recipe2 = Recipe("Salad", "Salad","Chop veggies, mix with dressing.",  [Image("salad_image.jpg")], 5)
    # recipe3 = Recipe("Soup", "Soup","Simmer ingredients for 30 mins.",  [Image("soup_image.jpg")], 3)
    #
    # # Adding recipes to the RecipeManager
    # cooking_assistant.recipes.addRecipe(recipe1)
    # cooking_assistant.recipes.addRecipe(recipe2)
    # cooking_assistant.recipes.addRecipe(recipe3)

    cooking_assistant.recipes.loadRecipesFromCSV("recipes.csv")

    # Displaying a recipe
    cooking_assistant.displayRecipe("Pasta")

    # Filtering recipes
    cooking_assistant.filterRecipes("salad")

    print()

    for i in cooking_assistant.recipes.recipes:
        print(i.getName())

    # cooking_assistant.recipes.saveRecipesToCSV("recipes.csv")
