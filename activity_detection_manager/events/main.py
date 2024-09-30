
# from common_utils.apis.base import BaseAPI
# from common_utils.state_machine.core import StateMachine



# events = [
#     {'depth': 4.5, 'brightness': 60, 'motion': 0.2},
#     {'depth': 3.5, 'brightness': 35, 'motion': 56},
#     {'depth': 1.8, 'brightness': 0.3, 'motion': 0.1},
# ]


# state_machine = StateMachine()

# for event in events:
#     state = state_machine.handle_event(event)
#     print(f"Current state: {state}")


from events.config.celery_utils import create_celery
from events.tasks.fetch_api.core import fetch_data


celery = create_celery()

celery.autodiscover_tasks(['events.tasks'])
    