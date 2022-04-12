from fastapi import FastAPI, status, Response
import vegan_checker as vc
import json, re

app = FastAPI()

print("loading json...")
with open('refined_foods.json', 'rb') as foods:
    data = json.load(foods)
print("done!")


@app.get("/")
async def root():
    return {"greeting": "welcome to the api!"}


@app.get("/food/{gtinUpc}")
async def get_ingd(gtinUpc, response: Response):
    try:
        result = data[gtinUpc]["ingredients"]
    except KeyError:
        result = {"err": f"No food with gtinUpc: {gtinUpc}"}
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result


@app.get("/vegan_ingredents/{gtinUpc}")
async def get_ingd(gtinUpc, response: Response):
    ingreds = await ing_spliter(data[gtinUpc]["ingredients"])
    try:
        not_vegan = await vc.contains_nonvegan(ingreds)
        maybe_vegan = await vc.contains_maybevegan(ingreds)
        vegan = [i for i in ingreds if i not in not_vegan and i not in maybe_vegan]
        result = {  
                    "name" : data[gtinUpc]["description"],
                    "not vegan" : not_vegan,
                    "maybe vegan" : maybe_vegan,
                    "vegan" : vegan
                }
    except KeyError:
        result = {"err": f"No food with gtinUpc: {gtinUpc}"}
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result


async def ing_spliter(ingredients):
    return re.split(r',\s*(?![^()]*\))', str(ingredients))
