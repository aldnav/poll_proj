from django import template

register = template.Library()

@register.filter(name='shortify')
def shortify(value):
	return value[:15]