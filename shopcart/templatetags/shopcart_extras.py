from django import template
register = template.Library()

@register.filter
def check_if_in_categorys(value,arg):
	if arg in value:
		return 'checked'
	else:
		return ''