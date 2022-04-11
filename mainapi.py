from fastapi import FastAPI, status, Response

app = FastAPI()


@app.get("/")
async def root():
    return {"greeting": "welcome to the api!"}


@app.get("/food/{gtinUpc}")
async def get_ingd(gtinUpc, response: Response):
    try:
        result = food[gtinUpc]
    except KeyError:
        result = {"err": f"No food with UUID: {uuid}"}
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result
