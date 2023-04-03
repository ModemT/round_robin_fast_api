from fastapi import FastAPI
import logging

app = FastAPI()

# Initialize logging configuration
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class AlternatingFailureApp:
    """
    An app that alternates between failing and succeeding on each request.
    """

    def __init__(self):
        self.failure_counter = 0

    def handle_request(self, data):
        """
        Handles the request by alternating between failing and returning the input data.

        Args:
            data: The input data to be handled.

        Returns:
            The input data if the app succeeded in handling the request.

        Raises:
            Exception: If the app failed to handle the request.
        """
        if self.failure_counter % 2 == 0:
            self.failure_counter += 1
            logging.error("App failure occurred")
            raise Exception("App failure")
        else:
            self.failure_counter += 1
            return data

alternating_failure_app = AlternatingFailureApp()

@app.post("/")
async def echo_request(data: dict):
    """
    A test endpoint that test the failure of the app.

    Args:
        data: The input data to be forwarded to the app.

    Returns:
        The output data returned by the app.

    Raises:
        Exception: If the app failed to handle the request.
    """
    return alternating_failure_app.handle_request(data)
