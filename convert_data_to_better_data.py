import json

data = {}

print("loading json...")
with open('FoodData_Central_branded_food_json_2021-10-28.json', 'rb') as foods:
    data = json.load(foods)
print("done!")

food = {}

i = 0
for item in data["BrandedFoods"]:
    if i % 10000 == 0:
        print(f'item {i} complete')
    i += 1

    food[item["gtinUpc"]] = item

print("dumping json...")
with open("refined_foods.json", "w") as outfile:
    json.dump(food, outfile)
print("done!")