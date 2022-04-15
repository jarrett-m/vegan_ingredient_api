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
    regex = re.compile('[^a-zA-Z\s-]')
    for ingredent in ingredients_to_check:
        regex.sub("", ingredent)
        for notvegan in nonvegan:
            if(findWholeWord(notvegan)(ingredent) is None):
                continue
            elif notvegan in ingredent:
                is_plant_based = False
                for plantbased_ing in plantbased:
                    if plantbased_ing in ingredent:
                        is_plant_based = True
                        break
                if not is_plant_based:
                    return_list.append(ingredent)
                    is_plant_based = False

            if ingredent in return_list:
                break

    return return_list

async def contains_maybevegan(ingredients_to_check):
    '''
    Takes an ingredients list as an argument and checks it agains the can-be-vegan list.
    If found returns a list with the may-be-vegan ingredients.
    '''
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []
    regex = re.compile('[^a-zA-Z\s-]')
    for ingredent in ingredients_to_check:
        regex.sub("", ingredent)
        for maybe_veg in maybevegan:
            if( findWholeWord(maybe_veg)(ingredent) is None):
                continue
            elif maybe_veg in ingredent:
                for plantbased_ing in plantbased:
                    if plantbased_ing in ingredent:
                        break
                    return_list.append(ingredent)
                    break
            if ingredent in return_list:
                break

    return return_list
'''
def contains_maybevegan(ingredients_to_check):
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []
    regex = re.compile('[^a-zA-Z\s-]')
    for ingredent in ingredients_to_check:
        regex.sub("", ingredent)
        for maybe_veg in maybevegan:
            if( findWholeWord(maybe_veg)(ingredent) is None):
                continue
            elif maybe_veg in ingredent:
                for plantbased_ing in plantbased:
                    if plantbased_ing in ingredent:
                        break
                    return_list.append(ingredent)
                    break
            if ingredent in return_list:
                break

    return return_list

def contains_nonvegan(ingredients_to_check): 
    ingredients_to_check = [i.strip().lower() for i in ingredients_to_check]
    return_list = []
    regex = re.compile('[^a-zA-Z\s-]')
    for ingredent in ingredients_to_check:
        regex.sub("", ingredent)
        for notvegan in nonvegan:
            if(findWholeWord(notvegan)(ingredent) is None):
                continue
            elif notvegan in ingredent:
                is_plant_based = False
                for plantbased_ing in plantbased:
                    if plantbased_ing in ingredent:
                        is_plant_based = True
                        break
                if not is_plant_based:
                    return_list.append(ingredent)
                    is_plant_based = False

            if ingredent in return_list:
                break

    return return_list

ingreds = ["almondmilk (filtered water, almonds)", "vitamin and mineral blend (calcium carbonate, vitamin e acetate, vitamin a palmitate, vitamin d2)", "sea salt", "locust bean gum" ,"gellan gum", "ascorbic acid (to protect freshness)", "natural flavor."]

not_vegan =  contains_nonvegan(ingreds)
maybe_vegan = contains_maybevegan(ingreds)
maybe_vegan = [ing for ing in maybe_vegan if ing not in not_vegan]
vegan =  [i for i in ingreds if i not in not_vegan and i not in maybe_vegan]

print(vegan)
print(maybe_vegan)
print(not_vegan)
'''