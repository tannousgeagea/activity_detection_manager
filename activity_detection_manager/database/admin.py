from django.contrib import admin
from .models import (
    State, 
    Condition, 
    Transition, 
    Configuration, 
    TransitionEntry,
    Service,
    )

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """
    Admin configuration for the State model.
    """
    list_display = ['name', 'description', 'created_at', 'updated_at'] 
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'updated_at']
    ordering = ['name']
    
@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Condition model.
    """
    list_display = ['left_operand', 'operator', 'right_operand', 'description', 'created_at']
    search_fields = ['left_operand', 'right_operand', 'description']
    list_filter = ['operator', 'created_at']
    ordering = ['left_operand']  

class ConditionInline(admin.TabularInline):
    """
    Inline for displaying and managing conditions within the TransitionEntry.
    """
    model = TransitionEntry.conditions.through 
    extra = 1 

@admin.register(TransitionEntry)
class TransitionEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TransitionEntry model.
    """
    list_display = ['from_state', 'to_state', 'show_conditions', 'updated_at']
    search_fields = ['from_state__name', 'to_state__name', 'description']
    list_filter = ['from_state', 'to_state', 'created_at', 'updated_at']
    ordering = ['from_state', 'to_state']
    inlines = [ConditionInline]
    filter_horizontal = ('conditions',)
    
    # Custom method to display the conditions in the list view
    def show_conditions(self, obj):
        """
        Display the conditions related to this TransitionEntry as a comma-separated string.
        """
        return ", ".join([f"{condition.left_operand} {condition.operator} {condition.right_operand}" for condition in obj.conditions.all()])
    
    show_conditions.short_description = "Conditions"  # Custom column title for the conditions

    
@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Transition model.
    """
    list_display = ['from_state', 'to_state', 'description', 'created_at', 'updated_at'] 
    search_fields = ['from_state__name', 'to_state__name', 'description']
    list_filter = ['from_state', 'to_state', 'created_at', 'updated_at']
    ordering = ['from_state', 'to_state']

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Configuration model.
    """
    list_display = ['key', 'value', 'description', 'created_at', 'updated_at']
    search_fields = ['key', 'description']
    list_filter = ['created_at', 'updated_at']
    ordering = ['key']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Service Model
    """
    list_display = ["name", "endpoint", "is_active", "created_at"]
    search_fields = ["name"]
    list_filter = ["name", "created_at", "is_active"]
    ordering = ["-created_at"]