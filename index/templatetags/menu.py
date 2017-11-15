from django import template
import re
import unidecode

from catalog.models import ProductFrom

register = template.Library()


# CUSTOM FILTERS
@register.simple_tag
def subcategory(param):
    sub_item = ProductFrom.objects.filter(category_id__slug=param)
    return sub_item

