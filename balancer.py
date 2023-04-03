from typing import List
import requests
from fastapi import FastAPI, Response
import time
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

class RoundRobinBalancer:
    """
    A class for load balancing requests using a round-robin algorithm and handling failed requests.

    Attributes:
        app_urls (List[str]): A list of URLs of the apps to load balance the requests to.
        current_index (int): The index of the next app URL to use in the round-robin algorithm.
        failed_apps (dict): A dictionary of app URLs and their retry times if they have failed.
        retry_downtime (int): The time in seconds to wait before retrying a failed app.
        max_delay_response (int): The maximum time in seconds to wait for a response from an app before timing out.
    """
    def __init__(self, app_urls: List[str]):
        self.app_urls = app_urls
        self.current_index = 0
        self.failed_apps = {}
        self.retry_downtime = 10
        self.max_delay_response = 2
    
    def get_next_app_url(self):
        """
        Gets the next app URL in the list using the round-robin algorithm, skipping any failed apps.

        Returns:
            str: The URL of the next app to use for the request.
        """
        url = self.app_urls[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.app_urls)
        while url in self.failed_apps and self.failed_apps[url] > time.monotonic():
            url = self.app_urls[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.app_urls)
        return url
    
    def mark_app_as_failed(self, app_url: str):
        """
        Marks an app as failed and sets the retry downtime.

        Args:
            app_url (str): The URL of the app to mark as failed.
        """
        self.failed_apps[app_url] = time.monotonic() + self.retry_downtime


balancer = RoundRobinBalancer(['http://localhost:8001', 'http://localhost:8002', 'http://localhost:8003'])

@app.post("/")
async def round_robin(data: dict, response: Response):
    """
    Sends a request to the next app URL using the round-robin algorithm.

    Args:
        data (dict): The data to send in the request.
        response (Response): The response object to add headers to.

    Returns:
        dict: The response data from the app.
    """
    app_url = balancer.get_next_app_url()
    while True:
        try:
            response_data = requests.post(app_url, json=data, timeout=balancer.max_delay_response).json()
            break
        except requests.exceptions.Timeout:
            logger.warning(f"Request to {app_url} timed out.")
            balancer.mark_app_as_failed(app_url)
            app_url = balancer.get_next_app_url()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request to {app_url} failed with exception: {e}")
            balancer.mark_app_as_failed(app_url)
            app_url = balancer.get_next_app_url()
    response.headers["X-App-URL"] = app_url
    return response_data
