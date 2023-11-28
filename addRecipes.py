import csv

# Sample data (with image paths)
recipes = [
    {
        "Recipe Name": "Enchilada Chicken Soup",
        "Ingredients": "1 can (10-3/4 ounces) condensed nacho cheese soup, undiluted",
        "Directions": "1. Cook spaghetti according to package directions. 2. In a skillet, cook pancetta until "
                      "crispy. 3. In a bowl, whisk eggs and grated Parmesan. 4. Drain cooked spaghetti and add to the "
                      "skillet with pancetta. 5. Remove from heat and quickly mix in egg mixture. 6. Season with "
                      "black pepper and salt. Serve immediately.",
        "Rating": 4.5,
        "Image Path": "RecipeImages/MOCKIMAGE.png"
    },
    # Add more recipes here...
]

# Define the CSV file name
file_name = "recipes.csv"

# Write data to the CSV file
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Recipe Name", "Ingredients", "Directions", "Rating", "Image Path"])

    # Write header
    writer.writeheader()

    # Write recipe data
    for recipe in recipes:
        writer.writerow(recipe)
