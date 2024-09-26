import os
import django
django.setup()

import logging
from celery import Celery
from celery import shared_task
from datetime import datetime, timedelta
from database.models import Service

from common_utils.apis.base import BaseAPI
from common_utils.service.core import ServiceManager
from common_utils.state_machine.core import StateMachine

services = Service.objects.filter(is_active=True)
fsm = StateMachine()

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='service-api:fetch_data')
def fetch_data(self, **kwargs):
    
    results = {}
    try:
        for service in services:
            service_manager = ServiceManager(
                service=service.name,
                url=f"{service.base_url}{service.endpoint}",
                auth_token=service.auth_token,
            )
            
            result = service_manager.get_data(
                gate_id=None
            )
            
            results = {
                **results,
                **result,
            }
            
        state = fsm.handle_event(event_data=results)
        print(state)    
        
    except Exception as err:
        logging.error(f"Error fetching data from service apis: {err}")
        


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='events_api.tasks.fetch_api.core.query_apis')
def query_apis(self, **kwargs):
    """
    Celery task that will run every second.
    """
    # Your logic to query APIs or process data
    print("Querying APIs every second!")
    # Example: Fetch data from APIs and process it
    return "API data fetched"