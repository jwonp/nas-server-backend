import os
from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def get_code_challenge():
    return settings.AUTH_DATA.get("CODE_CHALLENGE")


@register.simple_tag
def get_client_id():
    return settings.AUTH_DATA.get("CLIENT_ID")
