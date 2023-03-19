from django import template

register = template.Library()


@register.filter(name='split')
def split(value, key):
    return value.split(key)


@register.filter(name='value_subt')
def value_subt(val1, val2):
    return int(val1) - int(val2)
