from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Custom template filter to access dictionary items.
    Usage: {{ my_dict|get_item:key }}
    """
    return dictionary.get(key)


@register.filter(name='sub')
def subtract(dict1, dict2):
    """
    Custom template filter to subtract values from dictionaries.
    Usage: {{ dict1|sub:dict2 }}
    """
    result = {}
    for key in dict1.keys():
        result[key] = dict1.get(key, 0) - dict2.get(key, 0)
    return result
