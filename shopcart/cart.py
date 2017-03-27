#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Cart,Product,Cart_Products,System_Config,ExpressType,Address
from django.core.context_processors import csrf
from django.http import HttpResponse,JsonResponse
import json,uuid
from django.db import transaction
from shopcart.utils import get_system_parameters
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
from django.http import Http404
from django.template.response import TemplateResponse
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


def add_to_cart(request):
	ctx = {}
	ctx.update(csrf(request))
	result_dict = {}
	result_dict['message'] = ''
	if request.method =='POST':
		product_to_be_add = json.loads((request.body).decode())		
		
		#cart = None
		if request.user.is_authenticated():
			#找到这个用户的cart
			cart,object = Cart.objects.get_or_create(user=request.user)
			
		else:
			if 'cart_id' in request.COOKIES:
				cart_id = request.COOKIES["cart_id"]
				cart,created = Cart.objects.get_or_create(id=cart_id)
			else:
				cart = Cart.objects.create(user=None)
				
		product = Product.objects.get(id=product_to_be_add['product_id'])
		#如果商品有额外属性，则必须指定额外属性的条目
		
		product_attribute = None
		add_result_flag = True
		min_order_quantity = product.min_order_quantity #最小下单数量
		
		quantity_can_be_sold = product.quantity#库存
		
		logger.debug('The min_order_quantity of this product is :%s' % (min_order_quantity))
		try:
			product_attribute_id_to_be_add = int(product_to_be_add['product_attribute_id'])
		except Exception as err:
			logger.error('The product has muti values but not selected.')
			add_result_flag = False
		
		if product.attributes.all():
			if add_result_flag:
				for pa in product.attributes.all():
					#logger.debug('pa.id %s and product_attribute_id_to_be_add %s' % [str(pa.id),str(product_attribute_id_to_be_add)])
					if pa.id == product_attribute_id_to_be_add:
						product_attribute = pa
						#min_order_quantity = pa.min_order_quantity  #不控制pa的最小起订量了。
						quantity_can_be_sold = pa.quantity
						logger.debug('The min_order_quantity of this product has been changed to :%s' % (min_order_quantity))
						add_result_flag = True
						break
			else:
				#没选特定属性
				result_dict['message'] = _('Please select the product attributes!')
		else:
			#该商品没有多种属性，可以添加
			add_result_flag = True
				
		
		#判断加入购物车的数量数量否达到了最小下单数量，并且库存足够
		if add_result_flag:
			quantity = int(product_to_be_add['quantity'])
			if quantity < min_order_quantity:
				result_dict['success'] = False
				result_dict['message'] = _('The minimun order quantity of the product is %(value)s') % {'value': min_order_quantity}
				add_result_flag = False
			if quantity > quantity_can_be_sold:
				result_dict['success'] = False
				result_dict['message'] = _('Sorry, %(value)s pieces are in the stock only.') % {'value': quantity_can_be_sold}
				add_result_flag = False
				
		#判断商品是否已经上架
		if add_result_flag:
			if not product.is_publish:
				result_dict['success'] = False
				result_dict['message'] = _('Sorry , this item is not ready for sale !')
				add_result_flag = False
				
		
		if add_result_flag:
			cart_product,create = Cart_Products.objects.get_or_create(cart=cart,product=product,product_attribute=product_attribute)
			cart_product.quantity = cart_product.quantity + quantity
			cart_product.save()
		
			result_dict['success'] = True
			result_dict['message'] = _('Opration successful.')
		else:
			result_dict['success'] = False
			if not result_dict['message']:
				result_dict['message'] = _('Unknown Exception')
		
		#为了将cart_id写到cookie里，不得不用response对象，要不然可以简单的使用上面这句
		response = HttpResponse()
		response['Content-Type'] = "text/javascript"
		response.write(json.dumps(result_dict))
		response.set_cookie('cart_id',cart.id, max_age = 3600*24*365) 
		response.set_cookie('cart_item_type_count',cart.cart_products.all().count(),max_age = 3600 * 24 * 365)
		return response

def ajax_modify_cart(request):
	cart = json.loads((request.body).decode())
	#cart_to_find = {'cart_id':2}
	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = 'Parameter Error.'
	result_dict['cart_product_total'] = 0.00
	result_dict['sub_total'] = 0.00
	
	if 'method' in cart:
		if cart['method'] == 'clear':
			#这种情况下，cart_id代表购物车cart本身的id，不是购物车中每一条记录的id
			parent_cart = Cart.objects.get(id=cart['cart_id'])
			for cp in parent_cart.cart_products.all():
				cp.delete()
				
			result_dict['sub_total'] = parent_cart.get_sub_total()
			result_dict['success'] = True
			result_dict['message'] = _('Opration successful.')
			result_dict['cart_item_type_count'] = 0
			response = HttpResponse()
			response['Content-Type'] = "text/javascript"
			response.write(json.dumps(result_dict))
			response.set_cookie('cart_item_type_count',0,max_age = 3600 * 24 * 365)
			return response
		
		#如果不是clear，则表明cart_id代表的是购物车中每一笔记录的id
		try:
			cart_exist = Cart_Products.objects.get(id=cart['cart_id'])
		except:
			#记录没找到，则直接报错
			logger.info('cart %s not found.' % [cart['cart_id']])
			return JsonResponse(result_dict)
	
		if cart['method'] == 'add':
			cart_exist.quantity = cart_exist.quantity + int(cart['quantity'])
			cart_exist.save()
			#result_dict['cart_product_total'] = cart_exist.get_total()
			#result_dict['sub_total'] = cart_exist.cart.get_sub_total()
			if not set_cart_product_quantity(quantity,cart_exist,result_dict):
				return JsonResponse(result_dict)

		elif cart['method'] == 'sub':
			quantity = cart_exist.quantity - int(cart['quantity'])
			#不可减到1个以下
			if cart_exist.quantity <= 0:
				cart_exist.quantity = 1			
			if not set_cart_product_quantity(quantity,cart_exist,result_dict):
				return JsonResponse(result_dict)

		elif cart['method'] == 'del':
			parent_cart = cart_exist.cart
			cart_exist.delete()
			result_dict['sub_total'] = parent_cart.get_sub_total()
			result_dict['success'] = True
			result_dict['cart_item_type_count'] = parent_cart.cart_products.all().count()
			response = HttpResponse()
			response['Content-Type'] = "text/javascript"
			response.write(json.dumps(result_dict))
			response.set_cookie('cart_item_type_count',parent_cart.cart_products.all().count(),max_age = 3600 * 24 * 365)
			return response
			
		elif cart['method'] == 'set':
			quantity = int(cart['quantity'])
			logger.debug('quantity:' + str(quantity))
			if not set_cart_product_quantity(quantity,cart_exist,result_dict):
				return JsonResponse(result_dict)
		else:
			return JsonResponse(result_dict)
			
		#如果上面没报错，则成功
		result_dict['success'] = True
		result_dict['message'] = _('Opration successful.')
	
	return JsonResponse(result_dict)


def quantity_check(cart_product,quantity):
	if cart_product.product_attribute:
		product_attribute = cart_product.product_attribute
		if quantity > product_attribute.quantity:
			return False,product_attribute.quantity
		else:
			return True,0
	else:
		product = cart_product.product
		if quantity > product.quantity:
			return False,product.quantity
		else:
			return True,0
	
def set_cart_product_quantity(quantity,cart_exist,result_dict):
	
	min_order_quantity = 0
	quantity_left = 0
	current_quantity = cart_exist.quantity
	if cart_exist.product_attribute:	
		#min_order_quantity = cart_exist.product_attribute.min_order_quantity
		#将最小下单量控制从sku转移到商品
		min_order_quantity = cart_exist.product.min_order_quantity
		
		quantity_left = cart_exist.product_attribute.quantity
		#logger.debug('cart_exist.product_attribute:%s' % (cart_exist.product_attribute.min_order_quantity))
	else:
		min_order_quantity = cart_exist.product.min_order_quantity
		quantity_left = cart_exist.product.quantity
		logger.debug('cart_exist.product:%s' % (cart_exist.product.min_order_quantity))
	#logger.debug('at least:' + str(min_order_quantity))
	
	
	if quantity >= min_order_quantity:
		if quantity <= quantity_left:
			cart_exist.quantity = quantity
			cart_exist.save()
			result_dict['cart_product_total'] = cart_exist.get_total()
			result_dict['cart_product_price'] = cart_exist.get_product_price()
			result_dict['sub_total'] = cart_exist.cart.get_sub_total()
			return True
		else:
			result_dict['success'] = False
			result_dict['available'] = quantity_left
			result_dict['origin'] = current_quantity
			result_dict['message'] = _('There is only %s pieces in stock.' % quantity_left)
			return False
	else:
		result_dict['message'] = 'The product must order more than %s' % (min_order_quantity)
		result_dict['origin'] = current_quantity
		return False

def view_cart(request):
	if 'cart_id' in request.COOKIES:
		cart_id = request.COOKIES["cart_id"]
		cart,created = Cart.objects.get_or_create(id=cart_id)
	else:
		if request.user.is_authenticated():
			cart,object = Cart.objects.get_or_create(user=request.user)
		else:
			cart = Cart.objects.create(user=None)

	if request.is_ajax():
		ret_dict = {}
		ret_dict['success'] = True
		ret_dict['item_type_count'] = cart.cart_products.all().count()
		
		
		from shopcart.serializer import serializer
		#serialized_cart = serializer(cart,datetime_format='string',output_type='dict',many=True)
		
		#先不返回购物车中商品信息
		serialized_cart = serializer(cart,datetime_format='string',output_type='dict',many=False)
		#logger.debug(serialized_cart)
		ret_dict['cart'] = serialized_cart
		return JsonResponse(ret_dict) 
		
	else:
		ctx = {}
		ctx['system_para'] = get_system_parameters()
		ctx['menu_products'] = get_menu_products()
		ctx['page_name'] = 'My Cart'
		if request.method =='GET':
			ctx['cart'] = cart
			response = TemplateResponse(request,System_Config.get_template_name() + '/cart_detail.html',ctx)
			response.set_cookie('cart_id',cart.id ,max_age = 3600*24*365)
			return response

@login_required()
def check_out(request): 
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Check Out'
	
	if request.method == 'POST':
		#得到cart_product_id
		cart_product_id_list = request.POST.getlist('cart_product_id',[])

		#添加快递选择
		express_list = ExpressType.objects.filter(is_in_use=True).filter(is_delete=False)
		#将各种方式的价格都计算出来
		for e in express_list:
			e.price_infact = calc_shipping_fee(cart_product_id_list,e)
		ctx['express_list'] = express_list
		
		ctx['default_express'] = ExpressType.objects.all()[0]
		promotion_code = request.POST.get('promotion_code','')
		
		prices,promotion = get_prices(cart_product_id_list=cart_product_id_list,express_type=ctx['default_express'],discount_code=promotion_code)
		
		ctx['product_list'] = prices['product_list']
		ctx['sub_total'] =  prices['sub_total']
		ctx['shipping'] = prices['shipping']
		ctx['discount'] = prices['discount']
		ctx['total'] = prices['total']
		
		#找出用户的地址簿
		myuser = request.user
		addresses_list = Address.objects.filter(user=myuser)
		if addresses_list:
			has_default = False
			for address in addresses_list:
				if address.is_default:
					logger.debug('Find a default address.')
					ctx['default_address'] = address
					has_default = True
					break;
				
			if not has_default:
				#随便给一个
				logger.debug('Do not a default address.')
				ctx['default_address'] = addresses_list[0]
			
		return TemplateResponse(request,System_Config.get_template_name() + '/check_out.html',ctx)
	else:
		return redirect(reverse('cart_view_cart'))

		
#重新计算价格，一般用于切换了快递公司，切换了地址，或者输入了优惠码
def re_calculate_price(request):
	ret_dict = {}
	ret_dict['success'] = False
	ret_dict['message'] = _('Unknown Exception')
	
	if request.method == 'GET':
		cart_product_id_list = request.GET.getlist('cart_product_id',[])
		express_id = request.GET.get('express','')
		promotion_code = request.GET.get('promotion_code_try','')
		try:
			express_type = ExpressType.objects.get(id=express_id)
		except Exception as err:
			logger.error('Can not find express_type which id is %s.' % (express_id) + str(err))
			return JsonResponse(ret_dict)
		prices,promotion = get_prices(cart_product_id_list=cart_product_id_list,express_type=express_type,discount_code=promotion_code)
		if promotion:
			ret_dict['is_promotion_code_valid'] = True
		else:
			ret_dict['is_promotion_code_valid'] = False
			ret_dict['message'] = 'The promotion code is not valid.'
		prices['product_list'] = None
		
		ret_dict['success'] = True
		ret_dict['prices'] = prices
	return JsonResponse(ret_dict)
	
def calc_shipping_fee(cart_product_id_list,express_type):
	cart_product_list = Cart_Products.objects.filter(id__in=cart_product_id_list)
	weight_total = 0.0
	stere_total = 0.0
	shipping_fee = 0.00 
	for cp in cart_product_list:
		weight_total = weight_total + cp.get_weight_total('kg')
		stere_total = stere_total + cp.get_stere_total('m')
	
	logger.debug('The order total weight is [%s] kg , total stere is [%s] m*m*m' % (weight_total,stere_total))
	
	weight_ship_fee = express_type.price_per_kilogram * weight_total
	stere_ship_fee = express_type.price_per_stere * stere_total
	
	list_fee = [express_type.price_fixed,weight_ship_fee,stere_ship_fee]
		
	logger.debug('fix_ship_fee is：%s,weight_ship_fee：%s,stere_ship_fee is:%s' % (express_type.price_fixed,weight_ship_fee,stere_ship_fee))
	
	if express_type.price_calc_type == 'fixed':
		shipping_fee = express_type.price_fixed
	elif express_type.price_calc_type == 'weight':
		shipping_fee = weight_ship_fee
	elif express_type.price_calc_type == 'stere':
		shipping_fee = stere_ship_fee
	elif express_type.price_calc_type == 'min':
		shipping_fee = min(list_fee)
	elif express_type.price_calc_type == 'max':
		shipping_fee = max(list_fee)
	else:
		#意外的参数，按照最贵的计算
		shipping_fee = max(list_fee)
	return shipping_fee
	
	
		
def get_prices(cart_product_id_list,discount_code='',express_type=None):
	logger.debug("cart_product_id_list:%s" % cart_product_id_list)
	cart_product_list = Cart_Products.objects.filter(id__in=cart_product_id_list)
	ret_dict = {}
	ret_dict['product_list'] = cart_product_list
	ret_dict['sub_total'] = 0.00
	ret_dict['shipping'] = 0.00
	ret_dict['total'] = 0.00
	
	discount = 0
	promotion = None
	promotion_valid = False
	
	logger.debug('discount_code:%s' % discount_code)
	if discount_code:
		logger.debug('check discount code')
		from shopcart.models import Promotion
		try:
			promotion = Promotion.objects.get(code=discount_code)
			promotion_valid = promotion.valid()
		except Exception as err:
			logger.info('Can not find the promotion code %s.\n Error Message: %s' % (discount_code,err))
	else:
		promotion_valid = True
	
	sub_total = 0.00
	
	for cp in cart_product_list:
		sub_total = sub_total + cp.get_total()
		#ret_dict['sub_total'] = ret_dict['sub_total'] + cp.get_total()
	
	total = sub_total
	logger.debug('sub_total:%s' % sub_total)
	logger.debug('promotion:%s' % promotion)
	
	if promotion_valid and promotion:
		if promotion.discount_type == Promotion.DISCOUNT_TYPE_SCALE:
			discount = sub_total * float(promotion.discount) / 100
			logger.debug('discount 1:%s' % discount)
		elif promotion.discount_type == Promotion.DISCOUNT_TYPE_FIXED:
			discount = float(promotion.discount)
			logger.debug('discount 2:%s' % discount)
		else:
			logger.debug('discount 3:%s' % 0)
			pass
			
	
	
	
	total = total - discount
	if total < 0:
		total = 0
	
	ret_dict['sub_total'] = sub_total
	ret_dict['discount'] = discount
	
	ret_dict['shipping'] = 	calc_shipping_fee(cart_product_id_list,express_type)
	
	ret_dict['total'] = total + ret_dict['shipping']
	return ret_dict,promotion_valid
		
		
		
		
		
		
		
		
		