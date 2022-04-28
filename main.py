from fastapi import FastAPI, status, Response, Request
import vegan_checker as vc
import re
import aiosqlite
import uvicorn


app = FastAPI()
auth_key = "testKey" #replace key

@app.get("/")
async def root():
    return "Welcome to the vegan check api!"


@app.get("/food/{gtinUpc}")
async def get_open_api_endpoint(gtinUpc, response: Response, req: Request):

    response = await authCheck(req, response) if await authCheck(req, response) is not None else None
    
    if response.status_code != status.HTTP_200_OK:
        result = {"err": "Unauthorized, gamer. better luck next time"}
        return result

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
async def get_open_api_endpoint(gtinUpc, response: Response, req: Request):

    response = await authCheck(req, response) if (await authCheck(req, response) is not None) else None

    if response.status_code != status.HTTP_200_OK:
        result = {"err": "Unauthorized, gamer. better luck next time"}
        return result

    try:
        connection_obj =  await aiosqlite.connect('foods.db')
        cursor_obj = await connection_obj.cursor()
        await cursor_obj.execute("SELECT ingredients, description FROM foods WHERE gtinUpc=?", (gtinUpc,))
        data = await cursor_obj.fetchall()

        ingreds = await siing_spliter(data[0][0])
        name = data[0][1]

        not_vegan = await vc.contains_nonvegan(ingreds)
        maybe_vegan = await vc.contains_maybevegan(ingreds)
        maybe_vegan = [ing.lower() for ing in maybe_vegan if ing not in not_vegan]
        vegan =  [i.lower() for i in ingreds if i not in not_vegan and i not in maybe_vegan]

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
    ingredients = ingredients.replace(";", ",")
    ingredients = ingredients.replace("[", "(")
    ingredients = ingredients.replace("]", ")")

    result = re.findall(r"(\w+?) \(\w+?\)", ingredients)

    ing = []
    for item in result:
        if '(' in item:
            more = re.findall('\(.*?\)', item)
            if len(more) > 0 and ',' in more[0]:
                new_split = more[0]
                ing += await ing_spliter(new_split[1:-1])
            else:
                ing.append(item.strip())
        else:
            ing.append(item.strip())
    return list(set(ing))

async def siing_spliter(ingredients):
    ingredients = ingredients.lower()
    ingredients = ingredients.replace(";", ",")
    ingredients = ingredients.replace("[", "(")
    ingredients = ingredients.replace("]", ")")

    result = []
    i = 0
    pos = 0
    parth_pos = 0
    parth_c_pos = 0
    parth_count = 0
    
    for char in ingredients:
    
        if char == "(":
            parth_count += 1
            if parth_count == 1:
                parth_pos = pos
    
        elif char == ")":
            parth_count -= 1
            if parth_count == 0:
                parth_c_pos = pos

        if parth_count == 0 and char == ",":
            i += 1
            if "(" in result[i-1] and "," in result[i-1]:
                recur_this = result[i-1]
                result.pop()
                result.extend(await siing_spliter(recur_this[parth_pos+2:parth_c_pos+1]))
                i = len(result)
                pos = 0
        else:    
            try:
                result[i] += char
                pos += 1
            except(IndexError):
                if char != " ":
                    result.append(char)
                    pos = 0
                else:
                    continue
    
    if "(" in result[-1] and "," in result[-1]:
        recur_this = result[-1]
        result.pop()
        result.extend(await siing_spliter(recur_this[parth_pos+2:parth_c_pos+1]))
        i = len(result)
        pos = 0

    return list(set(result))

async def authCheck(req, response):
    auth_token = req.headers["authorization"]

    if (auth_token != auth_key):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)