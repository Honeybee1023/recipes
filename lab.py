"""
6.101 Lab:
Recipes
"""

import pickle
import sys
# import typing # optional import
# import pprint # optional import

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!

def atomic_ingredient_costs(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary mapping each atomic food name to its cost.
    """
    dict = {}
    for food in recipes_db:
        if food[1] == "cow":
            print(food[0])
            print(food[1])
        if food[0] == "atomic":
            dict[food[1]] = food[2]
    return dict


def compound_ingredient_possibilities(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary that maps each compound food name to a
    list of all the ingredient lists associated with that name.
    """
    dict = {}
    for food in recipes_db:
        if food[0] == "compound":
            dict[food[1]] = []

    for food in recipes_db:
        if food[0] == "compound":
            dict[food[1]].append(food[2])
            
    return dict


def lowest_cost(recipes_db, food_name, avoid=None):
    """
    Given a recipes database and the name of a food (str), return the lowest
    cost of a full recipe for the given food item or None if there is no way
    to make the food_item.
    """

    new_recipes_db = recipes_db[:]

    if avoid:
        for food in recipes_db:
            if food[1] in set(avoid):
                new_recipes_db.remove(food)

    atomic_db = atomic_ingredient_costs(new_recipes_db)
    compound_db = compound_ingredient_possibilities(new_recipes_db)

    if food_name not in atomic_db.keys() and food_name not in compound_db.keys():
        return None
    
    if food_name in atomic_db.keys():
        return atomic_db[food_name]
    
    known_item_lowest_costs = {}
    curr_min_cost = None

    for recipe in compound_db[food_name]:
        recipe_cost = 0
        for ingredient in recipe:
            if ingredient[0] in known_item_lowest_costs.keys():
                recipe_cost+= known_item_lowest_costs[ingredient[0]] * ingredient[1]
            else:
                if lowest_cost(new_recipes_db, ingredient[0], avoid) == None:
                    recipe_cost = None
                    break
                known_item_lowest_costs[ingredient[0]] = lowest_cost(new_recipes_db, ingredient[0], avoid)
                recipe_cost+= known_item_lowest_costs[ingredient[0]] * ingredient[1]
        if not curr_min_cost:
            curr_min_cost = recipe_cost
        if recipe_cost and (recipe_cost < curr_min_cost or curr_min_cost < 0):
            curr_min_cost = recipe_cost
    
    return curr_min_cost

def scaled_recipe(recipe_dict, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    raise NotImplementedError


def add_recipes(recipe_dicts):
    """
    Given a list of recipe dictionaries that map atomic food items to quantities,
    return a new dictionary that maps each ingredient name
    to the sum of its quantities across the given recipe dictionaries.

    For example,
        add_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    raise NotImplementedError


def cheapest_flat_recipe(recipes_db, food_name):
    """
    Given a recipes database and the name of a food (str), return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    raise NotImplementedError


def combine_recipes(nested_recipes):
    """
    Given a list of lists of recipe dictionaries, where each inner list
    represents all the recipes for a certain ingredient, compute and return a
    list of recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    raise NotImplementedError


def all_flat_recipes(recipes_db, food_name):
    """
    Given a recipes database, the name of a food (str), produce a list (in any
    order) of all possible flat recipe dictionaries for that category.

    Returns an empty list if there are no possible recipes
    """
    raise NotImplementedError


if __name__ == "__main__":
    # load recipe databases from the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes_db = pickle.load(f)

    with open("test_recipes/dairy_recipes.pickle", "rb") as f:
        dairy_recipes_db = pickle.load(f)

    with open("test_recipes/cookie_recipes.pickle", "rb") as f:
        cookie_recipes_db = pickle.load(f)

    # you may add additional testing code here!
    atomic_db = atomic_ingredient_costs(example_recipes_db)
    # cost = 0
    # for value in atomic_db.values():
    #    cost += value
    # print(cost)

    compound_db = compound_ingredient_possibilities(example_recipes_db)
    # count = 0
    # for key in compound_db.keys():
    #     count += len(compound_db[key]) - 1
    # print(count)