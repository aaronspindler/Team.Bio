# import os

from django import template

register = template.Library()


@register.simple_tag
def is_github_actions():
    return True
