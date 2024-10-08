import os
import django
django.setup()

import logging
from celery import Celery
from celery import shared_task
from datetime import datetime, timedelta
from metadata.models import Service

from common_utils.service.core import ServiceManager
from common_utils.state_machine.core import StateMachine

DATETIME_FORMAT = "%Y-%m-%d %H-%M-%S"
services = Service.objects.filter(is_active=True)
fsm = StateMachine()

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='events.tasks.fetch_api.core.fetch_data')
def fetch_data(self, **kwargs):
    
    data:dict =  {}
    results = {}
    try:
        for service in services:
            service_manager = ServiceManager(
                service=service.name,
                url=f"{service.base_url}{service.endpoint}",
                auth_token=service.auth_token,
            )
            
            result = service_manager.get_data(
                location='gate03'
            )
        
            print(result)
            results = {
                **results,
                **result,
            }
            
        state = fsm.state
        if results:
            state = fsm.handle_event(event_data=results)
    
        data.update(
            {
                "action": "done",
                "time": datetime.now().strftime(DATETIME_FORMAT),
                "results": f"Current State: {state}"
            }
        )
    except Exception as err:
        logging.error(f"Error fetching data from service apis: {err}")
        data.update(
            {
                "action": "failed",
                "time": datetime.now().strftime(DATETIME_FORMAT),
                "results": f"Error: {err}",
            }
        )
        
    return data


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='events.tasks.fetch_api.core.query_apis')
def query_apis(self, **kwargs):
    """
    Celery task that will run every second.
    """
    # Your logic to query APIs or process data
    print("Querying APIs every second!")
    # Example: Fetch data from APIs and process it
    return "API data fetched"