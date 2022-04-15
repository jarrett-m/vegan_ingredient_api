from fastapi import FastAPI, status, Response
import vegan_checker as vc
import re
import aiosqlite


app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to the vegan check api!"


@app.get("/food/{gtinUpc}")
async def get_open_api_endpoint(gtinUpc, response: Response):
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
async def get_open_api_endpoint(gtinUpc, response: Response):
    try:
        connection_obj =  await aiosqlite.connect('foods.db')
        cursor_obj = await connection_obj.cursor()
        await cursor_obj.execute("SELECT ingredients, description FROM foods WHERE gtinUpc=?", (gtinUpc,))
        data = await cursor_obj.fetchall()

        ingreds = await ing_spliter(data[0][0])
        name = data[0][1]

        not_vegan = await vc.contains_nonvegan(ingreds)
        maybe_vegan = await vc.contains_maybevegan(ingreds)
        maybe_vegan = [ing for ing in maybe_vegan if ing not in not_vegan]
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

