from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='timestamp_to_time')
def timestamp_to_time(value):
    return datetime.fromtimestamp(int(value)).strftime('%H:%M:%S')
