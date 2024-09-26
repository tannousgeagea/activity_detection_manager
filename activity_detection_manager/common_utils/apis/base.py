# motion_api.py
import logging
import requests
from requests.exceptions import HTTPError

class BaseAPI:
    url:str=None

    def get(self, params):
        results = {}
        try:
            response = requests.get(url=self.url, params=params)
            results = response.json()
        except HTTPError as err:
            logging.error(f"HTTPError getting data from {self.url}: {err}")
        except Exception as err:
            logging.error(f"Exeception Error getting data from {self.url}: {err}")
            
        return  results
        