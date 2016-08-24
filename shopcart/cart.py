#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Cart,Product,Cart_Products,System_Config,ExpressType,Address
from django.core.context_processors import csrf
from django.http import HttpResponse,JsonResponse
import json,uuid
from django.db import transaction
from shopcart.utils import System_Para,get_system_parameters
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
from django.http import Http404
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
						min_order_quantity = pa.min_order_quantity
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
			result_dict['cart_product_total'] = cart_exist.get_total()
			result_dict['sub_total'] = cart_exist.cart.get_sub_total()
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

	
def set_cart_product_quantity(quantity,cart_exist,result_dict):
	
	min_order_quantity = 0
	if cart_exist.product_attribute:	
		min_order_quantity = cart_exist.product_attribute.min_order_quantity
		logger.debug('cart_exist.product_attribute:%s' % (cart_exist.product_attribute.min_order_quantity))
	else:
		min_order_quantity = cart_exist.product.min_order_quantity
		logger.debug('cart_exist.product:%s' % (cart_exist.product.min_order_quantity))
	logger.debug('at least:' + str(min_order_quantity))
	
	
	if quantity >= min_order_quantity:
		cart_exist.quantity = quantity
		cart_exist.save()
		result_dict['cart_product_total'] = cart_exist.get_total()
		result_dict['sub_total'] = cart_exist.cart.get_sub_total()
		return True
	else:
		result_dict['message'] = 'The product must order more than %s' % (min_order_quantity)
		result_dict['origin'] = cart_exist.quantity
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
			response = render(request,System_Config.get_template_name() + '/cart_detail.html',ctx)
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
		ctx['express_list'] = ExpressType.objects.all()		
		
		ctx['default_express'] = ExpressType.objects.all()[0]
		
		prices = get_prices(cart_product_id_list=cart_product_id_list,express_type=ctx['default_express'])
		
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
			
		return render(request,System_Config.get_template_name() + '/check_out.html',ctx)
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
		try:
			express_type = ExpressType.objects.get(id=express_id)
		except Exception as err:
			logger.error('Can not find express_type which id is %s.' % (express_id) + str(err))
			return JsonResponse(ret_dict)
		prices = get_prices(cart_product_id_list=cart_product_id_list,express_type=express_type)
		#将商品详细情况去掉，不需要
		prices['product_list'] = None
		ret_dict['success'] = True
		ret_dict['message'] = prices
	return JsonResponse(ret_dict)
		
def get_prices(cart_product_id_list,discount=0.0,express_type=None,express_mode='fixed'):
	cart_product_list = Cart_Products.objects.filter(id__in=cart_product_id_list)
	ret_dict = {}
	ret_dict['product_list'] = cart_product_list
	ret_dict['sub_total'] = 0.00
	ret_dict['shipping'] = 0.00
	ret_dict['discount'] = discount
	ret_dict['total'] = 0.00
	
	for cp in cart_product_list:
		ret_dict['sub_total'] = ret_dict['sub_total'] + cp.get_total()
		
	if express_type:
		if express_mode == 'fixed':
			ret_dict['shipping'] = express_type.price_fixed
	
	ret_dict['total'] = ret_dict['sub_total'] + ret_dict['shipping'] - ret_dict['discount']
	return ret_dict
		
		
		
		
		
		
		
		
		