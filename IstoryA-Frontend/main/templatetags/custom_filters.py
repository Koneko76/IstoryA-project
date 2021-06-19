import base64
from django import template

register = template.Library()

@register.filter(name='binary_to_image')
def encode_binary_data_to_image(binary):
    res = base64.b64encode(binary)
    res = res.decode("utf-8")
    return res