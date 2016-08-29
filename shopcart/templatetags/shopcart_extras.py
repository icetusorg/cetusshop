from django import template
register = template.Library()

@register.filter
def check_if_in_categorys(value,arg):
	cat = arg
	if arg and value:	
		if arg.id in value:
			return 'checked'
	
	return ''
		
@register.filter
def check_if_in_product_attribute(value,arg):
	product = value
	for pa in product.attributes.all():
		if arg in pa.attribute.all():
			return 'checked'
	else:
		return ''