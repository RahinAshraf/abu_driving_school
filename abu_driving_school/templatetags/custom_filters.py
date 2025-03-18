# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def times(number):
    return range(number)


@register.filter
def to_list(value, count):
    """Generate a range list for the given count."""
    return range(count)


@register.filter
def to_list(value):
    """
    Converts an integer into a range object for template iteration.
    Ensures value is converted to an integer before passing to range().
    """
    try:
        return range(int(value))  # Ensure value is an integer
    except ValueError:
        return range(0)  # Return an empty range if there's a ValueError