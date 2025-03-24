# projects/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(value, arg):
    """Check if the value ends with the given string."""
    if value is not None and arg is not None:
        return value.endswith(arg)
    return False

@register.filter(name='split')
def split(value, arg):
    """Splits the value by the given delimiter and returns the desired part"""
    if value and arg:
        return value.split(arg)[-1]  # Return the last part after splitting by the delimiter
    return value