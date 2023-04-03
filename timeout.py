from fastapi import FastAPI
import time

app = FastAPI()

@app.post("/")
async def echo_request(data: dict):
    time.sleep(5)
    return data