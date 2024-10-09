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
            
        
    def post(self, url, params):
        try:
            
            print(f"Request to {url} ...", end='')
            response = requests.post(
                url=url,
                params=params
            )
            
            if response.status_code != 200:
                raise HTTPError(
                    f"HTTPError: {response.status_code}: {response.json()}"
                )
            
            print("Success!")
            
        except HTTPError as err:
            raise ValueError(f"HTTPError posting data to {url}: {err}")
        except Exception as err:
            raise ValueError(f"Exeception Error posting error to {url}: {err}")
            