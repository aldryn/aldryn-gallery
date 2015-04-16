import random

from django import template


register = template.Library()


@register.filter
def shuffle(arg):
    # slice it, cast it to list
    if arg:
        my_list = list(arg[:])
        random.shuffle(my_list)
        return my_list
    return []
