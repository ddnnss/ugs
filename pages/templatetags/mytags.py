from django import template


register = template.Library()


@register.filter
def format_card(data):
    try:
        temp = data.split(' ')
        print(temp)
        return f'{temp[0]} **** **** {temp[3]}'
    except:
        return 'Неверный номер карты'

