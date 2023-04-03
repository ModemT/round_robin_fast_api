from fastapi import FastAPI

app = FastAPI()

class AlternatingFailureApp:
    def __init__(self):
        self.failure_counter = 0
    
    def handle_request(self, data):
        if self.failure_counter % 2 == 0:
            self.failure_counter += 1
            raise Exception("App failure")
        else:
            self.failure_counter += 1
            return data

alternating_failure_app = AlternatingFailureApp()

@app.post("/")
async def echo_request(data: dict):
    return alternating_failure_app.handle_request(data)