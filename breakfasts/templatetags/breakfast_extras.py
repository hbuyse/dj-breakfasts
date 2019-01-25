# -*- coding: utf-8 -*-
"""Template tags for the `breakfasts` project."""

# Django
from django import template

register = template.Library()


@register.filter
def modulo(num, val):
    """Return the remainder from the euclidean division of num by val."""
    return num % val
