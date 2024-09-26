
import django
import logging
import requests
django.setup()

from datetime import datetime
from common_utils.apis.base import BaseAPI
from database.models import Service

DATETIME_FORMAT = "%Y-%m-%d %H-%M-%S"

class ServiceManager:
    def __init__(self, service, url, auth_token:str=None):
        self.api = BaseAPI(url=url) 
        self.service = service
        self.auth_token = auth_token
        
    def get_data(self, gate_id:str):
        """
        Calls each service defined in the database, retrieves the necessary data, and returns it.
        """
        results = {}
        dt = datetime.now().strftime(DATETIME_FORMAT)

        try:
            headers = {}
            if self.auth_token:
                headers['Authorization'] = f"Bearer {self.auth_token}"

            params = {
                "timestamp": dt,
                "gate_id": gate_id,
            }

            results = self.apis.get(params=params)

        except Exception as err:
            logging.error(f"Error calling api {self.api.url}: {err}")


        return results
