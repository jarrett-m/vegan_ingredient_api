import json

with open("maybevegan.json") as maybevegan_json:
    maybevegan = json.load(maybevegan_json)

with open("nonvegan.json") as maybevegan_json:
    nonvegan = json.load(maybevegan_json)

async def contains_maybevegan(ingredients_to_check):
    '''
    Takes an ingredients list as an argument and checks it agains the can-be-vegan list.
    If found returns a list with the may-be-vegan ingredients.
    '''
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []

    for ingredent in ingredients_to_check:
        for non_veg in nonvegan:
            if non_veg in ingredent:
                return_list.append(ingredent)
                break

    return return_list

async def contains_nonvegan(ingredients_to_check):
    '''
    Takes an ingredients list as an argument and checks it agains the can-be-vegan list.
    If found returns a list with the may-be-vegan ingredients.
    '''
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []

    for ingredent in ingredients_to_check:
        for maybe_veg in maybevegan:
            if maybe_veg in ingredent:
                return_list.append(ingredent)
                break

    return return_list

