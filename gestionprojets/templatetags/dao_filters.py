# Dans templatetags/dao_filters.py
from django import template

register = template.Library()


@register.filter
def get(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)
