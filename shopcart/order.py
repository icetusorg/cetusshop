#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,MyUser,Order,Address,Product,Order_Products,Cart_Products,Cart,Product_Attribute,ExpressType,OrderRemark
from shopcart.utils import System_Para,my_pagination,get_serial_number,get_system_parameters
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,Http404
import logging,json
from django.contrib.auth.decorators import login_required
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
from django.db import transaction
# Get an instance of a logger
import logging
logger = logging.getLogger('icetus.shopcart')

@login_required()
def ajax_cancel_order(request):
	order_to_cancel = json.loads((request.body).decode())
	result_dict = {}
	try:
		order = Order.objects.get(user=request.user,id=order_to_cancel['order_id'])
		order.status = Order.ORDER_STATUS_CANCLED
		order.save()
		result_dict['success'] = True
		result_dict['message'] = _('Opration successful.')
		return JsonResponse(result_dict)
	except:
		logger.error('Order was not found. Order_id：%s , user_id: %s' % [str(order_to_cancel.order_id),str(request.user.id)])
		result_dict['success'] = False
		result_dict['message'] = _('Parameter Error.')
		return JsonResponse(result_dict)

@login_required()
@transaction.atomic()
def place_order(request):
	logger.info('Start to place order.')
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Place Order'
	if request.method == 'POST':
		logger.debug('address_id:' + str(request.POST['address_id']))
		try:
			address = Address.objects.get(id=request.POST['address_id'])
		except:
			ctx['content'] = _('Address is not correct')
			return render(request,System_Config.get_template_name() + '/info_show.html',ctx)
			
		if address not in request.user.addresses.all():
			#如果这个地址不是这个用户的，报错
			ctx['content'] = 'System Error.Please try again.'
			return render(request,System_Config.get_template_name() + '/info_show.html',ctx)
		
		#金额
		sub_total,shipping,discount,total,remark,express_type = request.POST['sub_total'],request.POST['shipping'],request.POST['discount'],request.POST['total'],request.POST['remark'],request.POST['express']
		logger.debug('>>>>>0:sub_total=' + str(sub_total))
		#生成主订单
		logger.debug('>>>>>1')
		order = Order.objects.create(order_number=get_serial_number(),user=request.user,status=Order.ORDER_STATUS_PLACE_ORDER,country=address.country,province=address.province,city=address.city,district=address.district,address_line_1=address.address_line_1,
			address_line_2=address.address_line_2,first_name=address.first_name,last_name=address.last_name,zipcode=address.zipcode,tel=address.tel,mobile=address.mobile,email=request.user.email,
			products_amount = sub_total,shipping_fee=shipping,discount=discount,order_amount=total,to_seller=remark,express_type_name = ExpressType.objects.get(id=express_type).name)
			
		logger.debug('>>>>>2:order.id='+str(order.id))
		cart_product_id = request.POST.getlist('cart_product_id',[])
		logger.debug('>>>>>3:cart_product_id='+str(cart_product_id))
		
		#计算汇总金额
		amount_to_check = 0.00
		
		for cp_id in cart_product_id:
			cp = Cart_Products.objects.get(id=cp_id)
			
			amount_to_check = amount_to_check + cp.get_total()
			#向主订单加入商品
			logger.debug('>>>>>5:product.id='+str(cp.product.id))
			
			pa_id = None
			pa_name = ''
			pa_item_number = None
			if cp.product_attribute:
				pa_id = cp.product_attribute.id
				pa_name = cp.product_attribute.get_grouped_attribute_desc()
				pa_item_number = cp.product_attribute.sub_item_number
			
			
			op = Order_Products.objects.create(product_id=cp.product.id,product_attribute_id=pa_id,order=order,name=cp.product.name,short_desc=cp.product.short_desc,price=cp.get_product_price(),
				thumb=cp.product.thumb,image=cp.product.image,quantity=cp.quantity,product_attribute_name = pa_name,product_attribute_item_number=pa_item_number)

			logger.debug('>>>>>6:op.id='+str(op.id))
			# 20160614，考拉，加入了扣减库存的逻辑
			if cp.product_attribute:
				product_attribute = cp.product_attribute
				product_attribute.quantity = product_attribute.quantity - cp.quantity
				if product_attribute.quantity < 0:
					ctx['content'] = 'The product "%s" is sold out.' % product_attribute.product.name
					ctx['backurl'] = '/cart/show/'
					return render(request,System_Config.get_template_name() + '/info_show.html',ctx)
				
					#raise Exception('The product "%s" is sold out.' % product_attribute.product.name)
				product_attribute.save()
			else:
				product = cp.product
				product.quantity = product.quantity - cp.quantity
				if product.quantity < 0:
					ctx['content'] = 'The product "%s" is sold out.' % product.name
					ctx['backurl'] = '/cart/show/'
					return render(request,System_Config.get_template_name() + '/info_show.html',ctx)
					#raise Exception('The product "%s" is sold out.' % product.name)
				product.save()
			
			
			#删除购物车中商品
			cp.delete()
			logger.debug('>>>>>8:cp.delete')
		
		#TODO:校验总金额是否正确，不正确则抛出异常
		logger.debug('>>>>>9:amount_to_check=' + str(amount_to_check))
		if abs(amount_to_check-float(sub_total)) > 0.01: #浮点数比较，没法直接用 ==
			raise Exception('System error.Please try again.')
		
		return redirect('/cart/payment/' + str(order.id))

		
@transaction.atomic()
def payment(request,order_id):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Payment'
	
	order = Order.objects.get(id=order_id)
	
	ctx['paypal_account'] = System_Config.objects.get(name='paypal_account').val
	ctx['item_name'] = 'Your order:' + str(order.order_number) + " in " + System_Config.objects.get(name='site_name').val
	ctx['custom'] = order.order_number #向paypal传送本地订单编号
	ctx['amount'] = order.order_amount
	ctx['return_url'] =  System_Config.objects.get(name='base_url').val + "/order/show/"
	ctx['cancel_url'] = System_Config.objects.get(name='base_url').val + "/order/show/"
	ctx['notify_url'] = System_Config.objects.get(name='base_url').val + reverse('paypal-ipn')
	ctx['cmd'] = '_xclick'
	ctx['currency_code'] = System_Config.objects.get(name='default_currency').val
	ctx['charset'] = 'utf-8'
	ctx['rm'] = '1'
	
	
	paypal_env = 'sandbox'
	try:
		paypal_env = System_Config.objects.get(name='paypal_env').val
	except:
		logger.info('"paypal_env" is not definded,use default value : "sandbox".Please set the system parameter paypal_env = live if you want to use the paypal live service.')
	if paypal_env == 'live':
		ctx['paypal_action_url'] = 'https://www.paypal.com/cgi-bin/websc'
	else:
		ctx['paypal_action_url'] = 'https://www.sandbox.paypal.com/cgi-bin/websc'
	
	return render(request,System_Config.get_template_name() + '/payment.html',ctx)		

	
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
@receiver(valid_ipn_received)
def paypal_notify(sender, **kwargs):
	logger.debug(str('进入paypal通知处理程序'))
	ipn_obj = sender
	logger.debug(str('STEP_0:找出订单，检查状态，避免重复处理'))
	order = None
	try:
		order = Order.objects.get(order_number=ipn_obj.custom)
	except Exception as e:
		logger.debug('订单未找到：' + str(ipn_obj.custom))
		return
	
	logger.debug(str('STEP_1:校验总金额是否正确'))
	if abs(float(ipn_obj.mc_gross)-order.order_amount) > 0.01:
		logger.debug(str('总金额校验不正确。订单编号[%s]的总金额为[%s],实际支付金额为[%s]' % [order.order_number,order.order_amount,ipn_obj.mc_gross]))
		reason = 'amount not equal'
		detail = str('总金额校验不正确。订单ID[%s]的总金额为[%s],实际支付金额为[%s]' % [order.id,order.order_amount,ipn_obj.mc_gross])
		logger.debug(detail)
		logger.debug(str('记录到异常订单中，可能存在金额被篡改的情况'))
		abnormal_order = Abnormal_Order.create(order=order,reason=reason,detail=detail)
		order.status = Order.ORDER_STATUS_ERROR
		order.pay_status = 'Payment amount not equal'
		order.save()
		return
	logger.debug(str('STEP_3:校验收款账户是否是配置的账户'))
	paypal_account = System_Config.objects.get(name='paypal_account').val
	if ipn_obj.receiver_email != paypal_account:
		logger.debug(str('收款账户不正确。订单编号[%s]的实际收款账户为[%s]，配置的收款账户为：[%s]' % [order.order_number,ipn_obj.receiver_email,paypal_account]))
		reason = 'receiver not correct'
		detail = str('收款账户不正确。订单ID[%s]的实际收款账户为[%s]，配置的收款账户为：[%s]' % [ipn_obj.receiver_email,paypal_account])
		logger.debug(detail)
		abnormal_order = Abnormal_Order.create(order=order,reason=reason,detail=detail)
		order.status = Order.ORDER_STATUS_ERROR
		order.pay_status = 'Payment receiver not correct'
		order.save()
		return

	logger.debug(str('STEP_4:校验通过，修改订单状态为支付成功'))
	order.status = Order.ORDER_STATUS_PAYED_SUCCESS
	order.pay_status = 'Paid Successfully'
	order.save()
	
	#触发付款成功的事件
	from shopcart import signals
	signals.order_was_payed.send(sender="Order",order=order)
	return

@login_required()
def show_order(request):
	logger.info('Start to show order.')
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'My Orders'
	if request.method == 'GET':
		order_list = Order.objects.filter(user=request.user)
		
		try:
			order_list_page_size = System_Config.objects.get('order_list_page_size')
		except:
			logger.debug('order_list_page_size is not defined,use the default value 10.')
			order_list_page_size = 10
		order_list, page_range = my_pagination(request, order_list,display_amount=order_list_page_size)
		ctx['order_list'] = order_list
		ctx['page_range'] = page_range
		return render(request,System_Config.get_template_name() + '/orders.html',ctx)
		
		
@login_required()
def order_detail(request,id):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'My Orders'
	if request.method == 'GET':
		try:
			order = Order.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find order %s' % (id))
			raise Http404

		ctx['order'] = order
		return render(request,System_Config.get_template_name() + '/order_view.html',ctx)
		
		
@login_required()		
def list_order_remark(request,order_no):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'My Orders'
	remark_list = OrderRemark.objects.filter(order__order_number=order_no)
	if request.user.has_perm('shopcart.can_list_order_remark'):
		ctx['remark_list'] = remark_list
	else:
		ctx['remark_list'] = ''
	
	return HttpResponse(str(remark_list))

	