from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Splits a string by the given key/delimiter
    """
    return value.split(key)

@register.simple_tag
def fetch_file(key):
    if key:
        return default_storage.url(key)
    return ""

@register.simple_tag
def merge_strings(*args):
    merged = ""
    for arg in args:
        if isinstance(arg, str):
            merged += arg

    return merged