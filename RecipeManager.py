import csv


class Image:
    def __init__(self, imagePath):
        self.imagePath = imagePath

    def getImagePath(self):
        return self.imagePath

    def setImagePath(self, imagePath):
        self.imagePath = imagePath


class Recipe:
    def __init__(self, name, ingredients, instructions, rating=0, images=None):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.rating = rating
        self.images = images if images else []

    def getName(self):
        return self.name

    def getIngredients(self):
        return self.ingredients

    def getInstructions(self):
        return self.instructions

    def getImages(self):
        return self.images

    def getRating(self):
        return self.rating

    def setName(self, name):
        self.name = name

    def setIngredients(self, ingredients):
        self.ingredients = ingredients

    def setInstructions(self, instructions):
        self.instructions = instructions

    def setRating(self, rating):
        self.rating = rating

    def setImages(self, imagesPath):
        self.images = Image(imagesPath)


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

    def saveRecipesToCSV(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for recipe in self.recipes:
                writer.writerow([
                    recipe.getName(),
                    recipe.getIngredients(),
                    recipe.getInstructions(),
                    recipe.getRating(),
                    ', '.join([image.getImagePath() for image in recipe.getImages()])
                ])

    def loadRecipesFromCSV(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, ingredients, instructions, rating, image_paths = row
                images = [Image(path.strip()) for path in image_paths.split(',')]
                self.addRecipe(Recipe(name, ingredients, instructions,int(rating), images))
