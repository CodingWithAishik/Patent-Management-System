from django import template
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary.
    Usage: {{ mydict|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key, '')


@register.filter
def normalize_date(value):
    """
    Normalize date formats to dd/mm/yyyy.
    Handles formats like dd.mm.yyyy, dd-mm-yyyy, dd/mm/yyyy
    Usage: {{ date_field|normalize_date }}
    """
    if not value:
        return value
    
    # Convert to string if not already
    value = str(value).strip()
    
    # Replace dots and hyphens with slashes
    normalized = value.replace('.', '/').replace('-', '/')
    
    return normalized


@register.filter
def truncate_smart(value, length=100):
    """
    Truncate text smartly for display.
    Returns the value and a flag if truncated.
    Usage: {{ text|truncate_smart:100 }}
    """
    if not value:
        return value
    
    value = str(value)
    if len(value) <= length:
        return value
    
    return value[:length] + '...'
