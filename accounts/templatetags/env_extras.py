import os

from django import template

register = template.Library()


@register.simple_tag
def is_github_actions():
    return os.environ.get("GITHUB_ACTIONS", False)
