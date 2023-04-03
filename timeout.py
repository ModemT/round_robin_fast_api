from fastapi import FastAPI
import time

app = FastAPI()

@app.post("/")
async def echo_request(data: dict):
    """
    A test endpoint that simulates a delayed response of 5 seconds.

    Args:
        data (dict): A dictionary of data to be echoed back in the response.

    Returns:
        dict: A dictionary containing the same data as the input.
    """
    time.sleep(5)
    return data