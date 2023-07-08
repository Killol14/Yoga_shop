""" This Code Is from Code Institute and Django custom Template """

from django import template


register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
