from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
        """
        Allows accessing a dictionary item by key in a Django template.
        Usage: {{ my_dict|get_item:my_key }}
        """
        return dictionary.get(key)
    
