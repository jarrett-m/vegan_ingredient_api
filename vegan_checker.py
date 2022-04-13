import json
import re

with open("maybevegan.json") as maybevegan_json:
    maybevegan = json.load(maybevegan_json)

with open("nonvegan.json") as maybevegan_json:
    nonvegan = json.load(maybevegan_json)

with open("plantbasedversions.json") as plantbased_json:
    plantbased = json.load(plantbased_json)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

async def contains_nonvegan(ingredients_to_check):
    '''
    Takes an ingredients list as an argument and checks it agains the can-be-vegan list.
    If found returns a list with the may-be-vegan ingredients.
    '''
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []
    for ingredent in ingredients_to_check:
        for notvegan in nonvegan:
            if(findWholeWord(notvegan)(ingredent) is None):
                continue
            elif notvegan in ingredent:
                for plantbased_ing in plantbased:
                    if plantbased_ing in ingredent:
                        break
                    return_list.append(ingredent)
                    break

    return return_list

async def contains_maybevegan(ingredients_to_check):
    '''
    Takes an ingredients list as an argument and checks it agains the can-be-vegan list.
    If found returns a list with the may-be-vegan ingredients.
    '''
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []
    for ingredent in ingredients_to_check:
        for maybe_veg in maybevegan:
            if(findWholeWord(maybe_veg)(ingredent) is None):
                continue
            elif maybe_veg in ingredent:
                for plantbased_ing in plantbased:
                    if plantbased_ing in ingredent:
                        break
                    return_list.append(ingredent)
                    break

    return return_list

'''
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def test(ingredients_to_check):
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []
    for ingredent in ingredients_to_check:
        for maybe_veg in maybevegan:
            if(findWholeWord(maybe_veg)(ingredent) is None):
                print("")
            elif maybe_veg in ingredent:
                for plantbased_ing in plantbased:
                    if plantbased_ing in ingredent:
                        break
                    return_list.append(ingredent)
                    break

    return return_list
'''
