from fastapi import FastAPI, status, Response
import json

app = FastAPI()

with open('refined_foods.json', 'rb') as foods:
    data = json.load(foods)
    print("done reading JSON...")


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
