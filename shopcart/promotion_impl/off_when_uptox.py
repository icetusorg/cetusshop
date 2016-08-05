#coding=utf-8
from shopcart.promotion_impl.common_function import is_valid
import logging
logger = logging.getLogger('icetus.shopcart')

# 满减优惠实现类
def calculate(request,promotion):
	ret = {}
	ret['success'] = True
	ret['discount_amount'] = 0.0
	ret['message'] = ''
	
	#判断是否有效
	if is_valid(promotion):
		logger.info('The promotion is valid.')
	else:
		ret['message'] = 'The promotion code is not valid.'
		ret['success'] = False
		ret['discount_amount'] = 0.0
		return ret
	
	#开始计算满减
	discount_condition = promotion.discount_condition
	
	#优惠对象类型
	item_type = promotion.item_type
	
	if item_type.upper() == 'ORDER':
		#针对订单优惠
		cart_product_id = request.POST.getlist('cart_product_id',[])
		logger.debug('cart_product_id='+str(cart_product_id))
		#计算汇总金额
		total = 0.00
		shipping = float(request.POST.get('shipping','0.0'))
		total = total + shipping
		
		
		for cp_id in cart_product_id:
			from shopcart.models import Cart_Products
			cp = Cart_Products.objects.get(id=cp_id)
			total = total + cp.get_total()
		
		logger.debug('Total amount:%s' % (total) )
		
		if total >= float(discount_condition):
			ret['total'] = total - float(promotion.discount)
			ret['discount_amount'] = float(promotion.discount)
	else:
		pass
		
	return ret
	