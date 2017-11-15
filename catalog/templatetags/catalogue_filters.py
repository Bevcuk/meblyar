from django import template
import re
import unidecode

from catalog.models import ProductFrom

register = template.Library()


@register.simple_tag
def subcategory(param):
    sub_item = ProductFrom.objects.filter(category_id__slug=param)
    return sub_item


# CUSTOM FILTERS
@register.filter(name='to_string')
def to_string(param):
    return str(param)


@register.filter(name='index')
def index(List, i):
    return List[int(i) - 1]


@register.filter(name='partition_url')
def partition_url(value):
    return value.partition('_')[2]


@register.filter(name='split_by')
def split_by(value, sign):
    return value.split(sign)


# look if the page is already filtered
# if yes - check if one filter used or more
# if no - just use first filter

@register.filter(name='check_right_url')
def check_right_url(url, param):
    param_name = param.partition(',')[0]
    param_value = param.partition(',')[2]
    if '/filter/' and '=' in url:

        query_parts = url.partition('/filter/')

        full_query_parts = query_parts[2].split('/')
        # full_query_parts[0] - extra
        # full_query_parts[1] - price
        # full_query_parts[2] - other...

        extra_query_part = full_query_parts[0].split(';')
        query_dict = {}

        # створюємо словник з поточними параметрами виду - характеристика: [параметри, ]
        for i in extra_query_part:
            query_dict[i.partition('=')[0]] = i.partition('=')[2].split('_')

        # якщо характеристики нема - додаєм її
        if param_name not in query_dict.keys():
            query_dict[param_name] = []

        for key, value in query_dict.items():
            # якщо характеристика присутня і параметра ще нема - додаєм його
            if param_name == key and param_value not in value:
                value.append(param_value)
            # якщо характеристика присутня і такий параметр є  - видаляєм його
            elif param_name == key and param_value in value:
                value.remove(param_value)

        # видаляєм ключі(характеристики) з порожніми лістами
        query_dict = dict((k, v) for k, v in query_dict.items() if v)

        if len(query_dict) > 0:
            query_string = ''
            for key, value in query_dict.items():
                query_string += key + '=' + '_'.join(value) + ';'
            # видаляєм в кінці ';'
            query_string = query_string[:len(query_string) - 1]

            if 'from_' not in url:
                return query_parts[0] + query_parts[1] + query_string
            else:
                return query_parts[0] + query_parts[1] + query_string + '/' + full_query_parts[1]

        elif len(query_dict) == 0:
            if 'from_' not in url:
                return query_parts[0]
            else:
                return query_parts[0] + query_parts[1] + full_query_parts[1]

    elif '/filter/' in url and '=' not in url:
        query_parts = url.partition('/filter/')
        return query_parts[0] + query_parts[1] + param_name + '=' + param_value + '/' + query_parts[2]

    else:
        return url + '/filter/' + param_name + '=' + param_value


@register.filter(name='ctm_slugify')
def ctm_slugify(value):
    string = unidecode.unidecode(value).lower()
    return re.sub(r'\W+', '-', string)


@register.filter(name='check_if_url_contain')
def check_if_url_contain(url, param):
    param_name = param.partition(',')[0]
    param_value = param.partition(',')[2]

    query_parts = url.partition('/filter/')

    full_query_parts = query_parts[2].split('/')
    # full_query_parts[0] - extra
    # full_query_parts[1] - price
    # full_query_parts[2] - other...

    extra_query_part = full_query_parts[0].split(';')
    query_dict = {}

    # створюємо словник з поточними параметрами виду - характеристика: [параметри, ]
    for i in extra_query_part:
        query_dict[i.partition('=')[0]] = i.partition('=')[2].split('_')

    for key, value in query_dict.items():
        # якщо характеристика присутня і параметра ще нема - додаєм його
        if param_name == key and param_value not in value:
            return
        # якщо характеристика присутня і такий параметр є  - видаляєм його
        elif param_name == key and param_value in value:
            return 'class=active'


# CUSTOM TAGS
@register.simple_tag
def create_full_param(param_name, value):
    return param_name + ',' + value


@register.simple_tag
def full_name(kind, subkind):
    return kind + '_' + subkind
