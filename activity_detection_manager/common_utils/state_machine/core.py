import django
django.setup()

import operator
from database.models import (
    State, 
    Transition, 
    TransitionEntry, 
    Condition, 
    Configuration
    )

class StateMachine:
    def __init__(self):
        # Start in the initial state (e.g., NoTruck)
        self.state = State.objects.get(name='NoTruck')
        
        # Operator mapping to dynamically evaluate conditions
        self.operators = {
            '>': operator.gt,
            '<': operator.lt,
            '==': operator.eq,
            '!=': operator.ne,
            '>=': operator.ge,
            '<=': operator.le
        }

    def _evaluate_condition(self, condition: Condition, event_data: dict) -> bool:
        """
        Evaluate a single condition using event_data and configuration values.
        """
        left_value = event_data.get(condition.left_operand, None)
        right_value = (
            Configuration.objects.get(key=condition.right_operand).value 
            if condition.right_operand in Configuration.objects.values_list('key', flat=True)
            else condition.right_operand
        )
        
        return self.operators[condition.operator](float(left_value), float(right_value))

    def _evaluate_transition_entry(self, entry: TransitionEntry, event_data: dict) -> bool:
        """
        Evaluate all conditions for a TransitionEntry using AND logic.
        """
        return all(self._evaluate_condition(condition, event_data) for condition in entry.conditions.all())

    def handle_event(self, event_data: dict):
        """
        Handle the event and transition between states based on the conditions in the TransitionEntries.
        """
        # Get all possible transitions from the current state
        possible_transitions = Transition.objects.filter(from_state=self.state)
        for transition in possible_transitions:
            # Check all the TransitionEntries for the current transition
            entries = TransitionEntry.objects.filter(from_state=transition.from_state, to_state=transition.to_state)
            for entry in entries:
                if self._evaluate_transition_entry(entry, event_data):
                    print(f"Transitioning from {self.state} to {entry.to_state}")
                    self.state = entry.to_state
                    return self.state.name
        
        return self.state.name
