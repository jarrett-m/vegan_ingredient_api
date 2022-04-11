import json

data = {}

with open('FoodData_Central_branded_food_json_2021-10-28.json', 'rb') as foods:
    data = json.load(foods)

food = {}

print("done!")

i = 0
for item in data["BrandedFoods"]:
    if i % 10000 == 0:
        print(f'item {i} complete')
    i += 1

    food[item["gtinUpc"]] = item

i = 0
with open("refined_foods.json", "w") as outfile:
    if i % 10000 == 0:
        print(f'item {i} complete')
    i += 1
    json.dump(food, outfile)
