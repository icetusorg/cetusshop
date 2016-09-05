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

@register.filter		
def express_first_value(value,arg):
	express_list = value
	if express_list:
		item = express_list[0]
		if arg == 'name':
			return item.name
		if arg == 'id':
			return item.id
	
	return ''
	
@register.filter		
def equalornot(value,arg):
	arg_list = arg.split(',')
	
	if value == arg_list[0]:
		return arg_list[1]
	else:
		return arg_list[2]