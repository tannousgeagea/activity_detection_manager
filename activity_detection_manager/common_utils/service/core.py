
import django
import logging
import requests
django.setup()

from datetime import datetime
from common_utils.apis.base import BaseAPI

DATETIME_FORMAT = "%Y-%m-%d %H-%M-%S"

class ServiceManager:
    def __init__(self, service, url, auth_token:str=None):
        self.api = BaseAPI(url=url) 
        self.service = service
        self.auth_token = auth_token
        
    def get_data(self, location:str):
        """
        Calls each service defined in the database, retrieves the necessary data, and returns it.
        """
        results = {}
        dt = datetime.now() #.strftime(DATETIME_FORMAT)

        try:
            headers = {}
            if self.auth_token:
                headers['Authorization'] = f"Bearer {self.auth_token}"

            params = {
                "timestamp": dt,
                "location": location,
            }
                
            results = self.api.get(params=params)
            if 'status' in results.keys():
                results[f"{self.service}_status"] = results['status']

        except Exception as err:
            logging.error(f"Error calling api {self.api.url}: {err}")


        return results
