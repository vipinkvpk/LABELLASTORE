from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    try:
        return value - arg
    except TypeError:
        return 0  # or some default value or raise an error
