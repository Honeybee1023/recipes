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

    compound_db = compound_ingredient_possibilities(new_recipes_db)

    if food_name not in compound_db.keys():
        atomic_db = atomic_ingredient_costs(new_recipes_db)
        if food_name in atomic_db.keys():
            return atomic_db[food_name]
        else:
            return None
    
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
    new_dict = {}
    for key in recipe_dict.keys():
        new_dict[key] = recipe_dict[key] * n
    return new_dict


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
    new_dict = {}
    for dict in recipe_dicts:
        for item in dict.keys():
            if item in new_dict.keys():
                new_dict[item] += dict[item]
            else:
                new_dict[item] = dict[item]
    return new_dict


def cheapest_flat_recipe(recipes_db, food_name, avoid = None):
    """
    Given a recipes database and the name of a food (str), return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    new_recipes_db = recipes_db[:]

    if avoid:
        for food in recipes_db:
            if food[1] in set(avoid):
                new_recipes_db.remove(food)
    
    compound_db = compound_ingredient_possibilities(new_recipes_db)

    if food_name not in compound_db.keys():
        atomic_db = atomic_ingredient_costs(new_recipes_db)
        if food_name in atomic_db.keys():
            return {food_name: 1}
        else:
            return None
    
    known_item_lowest_costs = {}
    curr_min_cost = None
    
    for recipe in compound_db[food_name]:
        recipe_cost = 0
        list_of_dicts = []
        for ingredient in recipe:
            past_result = cheapest_flat_recipe(new_recipes_db, ingredient[0], avoid)
            if past_result == None:
                recipe_cost = None
                break
            else:
                list_of_dicts.append(scaled_recipe(past_result, ingredient[1]))
                past_cost = lowest_cost(new_recipes_db, ingredient[0], avoid)
                if past_cost == None:
                    recipe_cost = None
                    break
                else:
                    recipe_cost += past_cost * ingredient[1]
        if recipe_cost and recipe_cost == lowest_cost(new_recipes_db, food_name, avoid):
            return add_recipes(list_of_dicts)


def combine_recipes(nested_recipes):
    """
    Given a list of lists of recipe dictionaries, where each inner list
    represents all the recipes for a certain ingredient, compute and return a
    list of recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    if len(nested_recipes) == 0:
        return []
    if len(nested_recipes) == 1:
        return nested_recipes[0]
    first_list = nested_recipes[0]
    rest_of_lists = nested_recipes[1:]
    rest_combo = combine_recipes(rest_of_lists)
    return_list = []
    for dict1 in first_list:
        for dict2 in rest_combo:
            return_list.append(add_recipes([dict1, dict2]))
    return return_list

def all_flat_recipes(recipes_db, food_name, avoid = None):
    """
    Given a recipes database, the name of a food (str), produce a list (in any
    order) of all possible flat recipe dictionaries for that category.

    Returns an empty list if there are no possible recipes
    """
    new_recipes_db = recipes_db[:]

    if avoid:
        for food in recipes_db:
            if food[1] in set(avoid):
                new_recipes_db.remove(food)
    
    compound_db = compound_ingredient_possibilities(new_recipes_db)

    if food_name not in compound_db.keys():
        atomic_db = atomic_ingredient_costs(new_recipes_db)
        if food_name in atomic_db.keys():
            return [{food_name: 1}]
        else:
            return []
    
    output = []
    for recipe in compound_db[food_name]:
        nested_recipe = []
        for ingredient in recipe:
            nested_recipe.append([scaled_recipe(item, ingredient[1]) for item in all_flat_recipes(new_recipes_db, ingredient[0], avoid)])
        output.extend(combine_recipes(nested_recipe))

    return output

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

    #print(all_flat_recipes(cookie_recipes_db, 'cookie sandwich'))
    #print(all_flat_recipes(cookie_recipes_db, 'sugar'))
    #print(all_flat_recipes(cookie_recipes_db, 'cookie sandwich', ('sugar', 'chocolate ice cream')))
    #print(all_flat_recipes(cookie_recipes_db, 'cookie sandwich', ('cookie',)))

    cake_recipes = [{"cake": 1}, {"gluten free cake": 1}]
    icing_recipes = [{"vanilla icing": 1}, {"cream cheese icing": 1}]
    topping_recipes = [{"sprinkles": 20}]
    print(combine_recipes([cake_recipes, icing_recipes, topping_recipes]))
    
