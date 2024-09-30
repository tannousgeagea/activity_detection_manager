from django.db import models

# Create your models here.

class State(models.Model):
    """
    Represents a state in the state machine.
    Each state represents a point in the system's process.
    """
    name = models.CharField(max_length=255, unique=True)  # Name of the state, must be unique
    description = models.TextField(blank=True, null=True)  # Optional description of the state
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'state'  # Custom table name in the database
        verbose_name = 'State'  # Human-readable name for the admin interface
        verbose_name_plural = 'States'  # Plural form for admin interface
        ordering = ['name']  # Default ordering for querysets

    def __str__(self):
        return self.name  # Human-readable representation of the state



class Condition(models.Model):
    """
    Represents a condition used to trigger a transition.
    Example condition: 'depth > depth_threshold'
    """
    left_operand = models.CharField(max_length=255)  # e.g., depth, motion_score
    operator = models.CharField(max_length=10, choices=[
        ('>', 'Greater Than'),
        ('<', 'Less Than'),
        ('==', 'Equal'),
        ('!=', 'Not Equal'),
        ('>=', 'Greater or Equal'),
        ('<=', 'Less or Equal'),
    ])
    right_operand = models.CharField(max_length=255)  # e.g., depth_threshold, brightness_threshold
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'condition'
        verbose_name = 'Condition'
        verbose_name_plural = 'Conditions'
        ordering = ['left_operand']  # Default ordering for conditions in queries

    def __str__(self):
        return f"{self.left_operand} {self.operator} {self.right_operand}"

class Transition(models.Model):
    """
    Represents a state transition in the state machine.
    Each transition defines which conditions must be satisfied to move from one state to another.
    """
    from_state = models.ForeignKey(State, related_name='from_state', on_delete=models.CASCADE)
    to_state = models.ForeignKey(State, related_name='to_state', on_delete=models.CASCADE)
    # conditions = models.ManyToManyField(Condition, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transition'
        verbose_name = 'Transition' 
        verbose_name_plural = 'Transitions'
        unique_together = ('from_state', 'to_state')  # Ensures unique transitions between states
        ordering = ['from_state', 'to_state']  # Default ordering for queries

    def __str__(self):
        return f"Transition from {self.from_state} to {self.to_state}"

class TransitionEntry(models.Model):
    """
    Represents a single entry for a transition from one state to another.
    Each entry has its own set of conditions that must all be met (AND logic).
    Multiple entries for the same from_state to to_state use OR logic.
    """
    # from_state = models.ForeignKey(State, related_name='from_entries', on_delete=models.CASCADE)
    # to_state = models.ForeignKey(State, related_name='to_entries', on_delete=models.CASCADE)
    transition = models.ForeignKey(Transition, on_delete=models.CASCADE, related_name='transition')
    conditions = models.ManyToManyField(Condition, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transition_entry'
        verbose_name = 'Transition Entry'
        verbose_name_plural = 'Transition Entries'
        ordering = ['transition']

    def __str__(self):
        return f"Entry from {self.transition.from_state} to {self.transition.to_state}"

class Configuration(models.Model):
    """
    Stores the configurable thresholds for the state machine.
    """
    key = models.CharField(max_length=255, unique=True)  # e.g., depth_threshold, brightness_threshold
    value = models.FloatField()  # The actual value for the threshold
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'configuration' 
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configurations'
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value}"

class Service(models.Model):
    """
    Represents an external service (e.g., motion detection, depth estimation).
    """
    name = models.CharField(max_length=255, unique=True)
    base_url = models.CharField(max_length=255)
    endpoint = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=512, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'service' 
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name