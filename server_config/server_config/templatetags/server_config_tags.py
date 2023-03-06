import os
from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def get_env_var(key):
    return settings.AUTH_DATA.get(key.upper())
