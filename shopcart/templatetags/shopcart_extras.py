from django import template
register = template.Library()
import logging
logger = logging.getLogger('icetus.shopcart')

@register.filter
def is_blog(value,arg):
	if value:
		from shopcart.models import Article
		if value.category == Article.ARTICLE_CATEGORY_BLOG:
			return True
		else:
			return False
	else:
		if arg == Article.ARTICLE_CATEGORY_BLOG:
			return True
		else:
			return False
		

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
def currency_list(value,arg):
	if  value == 'USD':
		return '美元'
	elif value == 'RMB':	
		return '人民币'
	elif value == 'EUR':
		return '欧元'										
	else:
		return value	


@register.filter		
def promotion_type(value,arg):
	from shopcart.models import Promotion
	logger.debug('value: %s' % (value))
	logger.debug('Promotion.DISCOUNT_TYPE_FIXED: %s' % (Promotion.DISCOUNT_TYPE_FIXED))
	if  value == Promotion.DISCOUNT_TYPE_FIXED:
		return '直减'
	elif value == Promotion.DISCOUNT_TYPE_SCALE:	
		return '折扣'
	elif value == Promotion.DISCOUNT_TYPE_OFF_WHEN_UPTOX:
		return '满减'										
	else:
		return value		
		
		
@register.filter		
def express_type_list(value,arg):
	if  value == 'fixed':
		return '固定运费'
	elif value == 'weight':	
		return '按重量'
	elif value == 'stere':
		return '按体积'
	elif value == 'max':
		return '就高'
	elif value == 'min':
		return '就低'										
	else:
		return value

		
		

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
def is_equal(value,arg):
	if value == arg:
		return True
	else:
		return False
	
@register.filter		
def equalornot(value,arg):
	arg_list = arg.split(',')
	
	if value == arg_list[0]:
		return arg_list[1]
	else:
		return arg_list[2]
		
@register.filter
def admin_order_quert_item(value,arg):
	if  value == 'order_number':
		return '订单号'
	elif value == 'order_user_email':	
		return '用户名'											
	else:
		return value	
		
@register.filter
def admin_product_para_group(value,arg):
	if value:
		if  value.parameters.all().count() > 0:
			if arg == 'name':
				return value.parameters.all()[0].product_para.group.name
			else:
				return value.parameters.all()[0].product_para.group.id
		else:
			if arg=='name':
				return '请选择一个属性组'
			else:
				return ''
	else:
		if arg=='name':
			return '请选择一个属性组'
		else:
			return ''
		
@register.filter
def admin_product_price(value,arg):
	try:
		index = int(arg)
	except:
		return None
		
	if value:	
		if value.prices.all().count()>0:
			return value.prices.all()[index].price
		else:
			return 0.00
	else:
		return 0.00
		
@register.filter
def admin_product_price_quantity(value,arg):
	try:
		index = int(arg)
	except:
		return None
	
	if value:
		if value.prices.all().count()>0:
			return value.prices.all()[index].quantity
		else:
			return 0
	else:
		return 0
		
		
@register.filter
def admin_order_status(value,arg):
	if  value == '0':
		return '已下单'
	elif value == '10':	
		return '已付款'
	elif value == '18':
		return '部分发货'
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
def admin_login_url(value,arg):
	if value == '/admin/' or value == '/admin' or next == '':
		return '/admin/index/'
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