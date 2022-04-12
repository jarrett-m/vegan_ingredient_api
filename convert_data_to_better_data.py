import json
import sqlite3


data = {}

print("loading json...")
with open('FoodData_Central_branded_food_json_2021-10-28.json', 'rb') as foods:
    data = json.load(foods)
print("done!")

foods = {}

'''
i = 0
for item in data["BrandedFoods"]:
    if i % 10000 == 0:
        print(f'item {i} complete')
    i += 1

    foods[item["gtinUpc"]] = item
'''


#print("dumping json...")
#with open("refined_foods.json", "w") as outfile:
#    json.dump(food, outfile)
#print("done!")


i = 0
for item in data["BrandedFoods"]:
    if i % 10000 == 0:
        print(f'item {i} complete')
    i += 1

    newUPC = ''
    for num in item["gtinUpc"]:
        if num.isdigit():
            newUPC += num
        

    foods[newUPC] = {
        "gtinUpc": newUPC,
        "description": item["description"],
        "ingredients": item["ingredients"],
        "brandOwner": item["brandOwner"]
    }



connection_obj = sqlite3.connect('foods.db')
cursor_obj = connection_obj.cursor()
cursor_obj.execute("DROP TABLE IF EXISTS FOODS")
table = " CREATE TABLE FOODS (gtinUpc VARCHAR PRIMARY KEY, description VARCHAR(500) NOT NULL, ingredients VARCHAR(50000) NOT NULL, brandOwner VARCHAR(500)); "
cursor_obj.execute(table)

print("Table is Ready")

i = 0
for key in foods.keys():
    if i % 10000 == 0:
        print(f'item {i} complete')
    i += 1

    command = "INSERT or REPLACE INTO FOODS VALUES (?,?,?,?)"
    if key != '':
        cursor_obj.execute(command, [foods[key]["gtinUpc"], foods[key]["description"], foods[key]["ingredients"], foods[key]["brandOwner"]])

    #print(int(foods[key]["gtinUpc"]), foods[key]["description"], foods[key]["ingredients"], foods[key]["brandOwner"])
    #cursor_obj.execute(command, [int(foods[key]["gtinUpc"]), foods[key]["description"], foods[key]["ingredients"], foods[key]["brandOwner"]])
connection_obj.commit()
connection_obj.close()