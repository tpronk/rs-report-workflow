from core import NestedDataParser 

# Example dataset: two delicious recipes
recipes = [
    {
        "name": "Spaghetti Carbonara",
        "author": "Kertin Cziau",
        "ingredients": [
            "Pasta",
            "Eggs",
            "Pancetta",
            "Parmesan Cheese"
        ],
    },
    {
        "name": "Vegetable Stir-Fry",
        "ingredients": [
            "Broccoli",
            "Carrots",
            "Soy Sauce"
        ]
    }
]

# Resolve a JSON pointer to the name of the first recipe: Spaghetti Carbonara
print(NestedDataParser.resolve(recipes, [
    {'type': 'pointer', 'pointer': '/0/name'}
]))

# Get the number of recipes
print(NestedDataParser.resolve(recipes, [
    {'type': 'count'}
]))

# Get the ingredients of the second recipe joined by comma: Broccoli, Carrots, SoySauce
print(NestedDataParser.resolve(recipes, [
    {'type': 'pointer', 'pointer': '/1/ingredients'},
    {'type': 'join', 'separator': ', '}
]))

# Count the number of ingredients per recipe and join that by comma: 4, 3
print(NestedDataParser.resolve(recipes, [
    {'type': 'join', 'separator': ', '},
    {'type': 'pointer', 'pointer': '/ingredients'},
    {'type': 'count'},
]))

# Have a mapping return None if it encounters an exception: None
print(NestedDataParser.resolve(recipes, [
    {'type': 'pointer', 'pointer': '/doesnotexist', 'except': None},
]))

# Author per recipe joined by comma, using "John Doe" if no author is found: Kertin Cziau, John Doe
print(NestedDataParser.resolve(recipes, [
    {'type': 'join', 'separator': ', '},
    {'type': 'pointer', 'pointer': '/author', 'except': 'John Doe'},
]))