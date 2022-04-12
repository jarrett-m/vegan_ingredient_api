from select import select
from click import command
from fastapi import FastAPI, status, Response
import vegan_checker as vc
import json, re
import aiosqlite


app = FastAPI()

'''
print("loading json...")
with open('refined_foods.json', 'rb') as foods:
    data = json.load(foods)
print("done!")
'''



@app.get("/")
async def root():
    return {"greeting": "welcome to the api!"}


@app.get("/food/{gtinUpc}")
async def get_ingd(gtinUpc, response: Response):
    connection_obj =  await aiosqlite.connect('foods.db')
    cursor_obj = await connection_obj.cursor()
    try:
        await cursor_obj.execute("SELECT ingredients FROM foods WHERE gtinUpc=?", (gtinUpc,))
        result = await cursor_obj.fetchall()
        result = result[0]
    except KeyError:
        result = {"err": f"No food with gtinUpc: {gtinUpc}"}
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result


@app.get("/vegan_ingredents/{gtinUpc}")
async def get_ingd(gtinUpc, response: Response):

    try:
        connection_obj =  await aiosqlite.connect('foods.db')
        cursor_obj = await connection_obj.cursor()
        await cursor_obj.execute("SELECT ingredients, description FROM foods WHERE gtinUpc=?", (gtinUpc,))
        data = await cursor_obj.fetchall()

        ingreds = await ing_spliter(data[0][0])
        name = data[0][1]

        not_vegan = await vc.contains_nonvegan(ingreds)
        maybe_vegan = await vc.contains_maybevegan(ingreds)
        vegan =  [i for i in ingreds if i not in not_vegan and i not in maybe_vegan]
        result = {  
                    "name" : name,
                    "not vegan" : not_vegan,
                    "maybe vegan" : maybe_vegan,
                    "vegan" : vegan
                }

    except KeyError:
        result = {"err": f"No food with gtinUpc: {gtinUpc}"}
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result


async def ing_spliter(ingredients):
    ingredients = ingredients.lower()
    return re.split(r',\s*(?![^()]*\))', str(ingredients))
