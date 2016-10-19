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
def check_if_in_delivery_type(value,arg):
	type = value
	express = arg
	
	if express:
		if type in express.get_express_types():
			return True
	else:
		return False

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
		
@register.filter
def admin_order_status(value,arg):
	if  value == '0':
		return '已下单，待付款'
	elif value == '10':	
		return '已付款，待备货'
	elif value == '15':
		return '已备货，待发货'
	elif value == '20':
		return '已发货'
	elif value == '30':
		return '已完成'
	elif value == '90':
		return '异常'
	elif value == '99':
		return '已关闭'											
	else:
		return value
		
@register.filter
def admin_article_category(value,arg):
	if  value == '0':
		return '宣传博客'
	elif value == '10':	
		return '网站公告'
	elif value == '20':
		return '站点信息'										
	else:
		return value