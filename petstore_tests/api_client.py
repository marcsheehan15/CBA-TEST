import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIClient:
    BASE_URL = 'https://petstore.swagger.io/v2'

    def __init__(self):
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        logger.info(f"Sending GET request to {url} with params {params}")
        response = self.session.get(url, params=params)
        logger.info(f"Received response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, json=None, data=None, files=None):
        url = f"{self.BASE_URL}{endpoint}"
        logger.info(f"Sending POST request to {url} with data {data} and files {files}")
        response = self.session.post(url, json=json, data=data, files=files)
        logger.info(f"Received response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, json=None):
        url = f"{self.BASE_URL}{endpoint}"
        logger.info(f"Sending PUT request to {url} with data {json}")
        response = self.session.put(url, json=json)
        logger.info(f"Received response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        url = f"{self.BASE_URL}{endpoint}"
        logger.info(f"Sending DELETE request to {url}")
        response = self.session.delete(url)
        logger.info(f"Received response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.status_code
