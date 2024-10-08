# motion_api.py
import logging
import requests
from requests.exceptions import HTTPError
from dataclasses import dataclass



@dataclass
class BaseAPI:
    url:str=None

    def get(self, params):
        results = {}
        try:
            response = requests.get(url=self.url, params=params)
            
            if response.status_code != 200:
                err = response.json().get('error')
                raise HTTPError(
                    f"HttpError Occured: {response.status_code}: {err}"
                ) 
            
            results = response.json().get('data')
            return  results
        
        except HTTPError as err:
            raise ValueError(f"HTTPError getting data from {self.url}: {err}")
        except Exception as err:
            raise ValueError(f"Exeception Error getting data from {self.url}: {err}")
            
        