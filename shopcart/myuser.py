#coding=utf-8
#from shopcart.handler import sendmail
from django.shortcuts import render,redirect,render_to_response
from shopcart.models import System_Config,MyUser,Cart,Product,Cart_Products,Wish,Reset_Password,Address,Order,Order_Products,Abnormal_Order
from shopcart.utils import System_Para,my_pagination,add_captcha,my_send_mail,get_serial_number,get_system_parameters,customize_tdk
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from shopcart.forms import register_form,captcha_form,address_form,user_info_form
import json,uuid,datetime
from django.db import transaction
import requests
from six import b
from django.core.urlresolvers import reverse
from shopcart import signals
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
from django.http import Http404
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

# Create your views here.
def register(request):
	ctx = {}
	ctx.update(csrf(request))
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Regitser'
	ctx = add_captcha(ctx) #添加验证码
	logger.debug('Enter register function.')
	if request.method == 'GET':
		#GET请求，直接返回页面
		return render(request,System_Config.get_template_name() + '/register.html',ctx)
	else:
		form = register_form(request.POST) # 获取Post表单数据
		if form.is_valid():# 验证表单
			myuser = MyUser.objects.create_user(username=None,email=form.cleaned_data['email'].lower(),password=form.cleaned_data['password'],first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'])
			
			#触发用户注册成功的事件
			signals.user_registration_success.send(sender='MyUser',user=myuser)
			#return redirect('/user/login')
			
			#准备登陆
			myuser.password = form.cleaned_data['password']
			return inner_login(request,myuser)
		else:
			logger.error('form is not valid')
			ctx['reg_result'] = _('Registration faild.')
			return render(request,System_Config.get_template_name() + '/register.html',ctx)			
			

			
			
@login_required
def info(request):
	ctx = {}
	ctx.update(csrf(request))
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	if request.method == 'GET':
		#GET请求，直接返回页面
		return render(request,System_Config.get_template_name() + '/user_info.html',ctx)
	else:
		logger.debug("Modify User Info")
		form = user_info_form(request.POST) # 获取Post表单数据
		myuser = request.user
		if form.is_valid():# 验证表单
			myuser.first_name = form.cleaned_data['first_name']
			myuser.last_name = form.cleaned_data['last_name']
			logger.debug(myuser.last_name)
		else:
			logger.debug('not validate')
		if 'changePassword' in request.POST:
			#需要更改密码
			myuser.set_password(request.POST['password'])
		else:
			#不更改密码
			logger.debug('not checked')
		myuser.save()
		return redirect('/user/info/?success=true')

def do_login(request,myuser):
	if myuser is not None:
		auth.login(request,myuser)
		mycart = merge_cart(request)
		redirect_url = reverse('product_view_list')
		if 'next' in request.POST:
			if len(request.POST['next']) > 0:
				redirect_url = request.POST['next']
			
		response = redirect(redirect_url)
		response.set_cookie('cart_id',mycart.id,max_age = 3600*24*365)
		response.set_cookie('cart_item_type_count',mycart.cart_products.all().count(),max_age = 3600*24*365)
		response.set_cookie('icetususer',myuser.email)
		return response
	else:
		ctx['login_result'] = _('Your account name or password is incorrect.')
		return render(request,System_Config.get_template_name() + '/login.html',ctx)	

def inner_login(request,login_user):
	myuser = None
	if login_user:
		myuser = auth.authenticate(username = login_user.email, password = login_user.password)
	return do_login(request,myuser)

def login(request,tdk=None):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Login'
	ctx = add_captcha(ctx) #添加验证码
	customize_tdk(ctx,tdk)
	if request.method == 'GET':
		#GET请求，直接返回页面
		if 'next' in request.GET:
			ctx['next'] = request.GET['next']
		return render(request,System_Config.get_template_name() + '/login.html',ctx)
	else:	
		ctx.update(csrf(request))
		form = captcha_form(request.POST) # 获取Post表单数据
		if 'next' in request.POST:
			next = request.POST['next']
			ctx['next'] = next
			
		#if form.is_valid():# 验证表单,会自动验证验证码，（新版不要验证码了）
		myuser = auth.authenticate(username = request.POST['email'].lower(), password = request.POST['password'])
		return do_login(request,myuser)
		#else:
		#	ctx['login_result'] = _('Please check you input.')
		#	return render(request,System_Config.get_template_name() + '/login.html',ctx)
			

def merge_cart(request):
	#检查cookie中是否有cart_id，如果没有，直接用user的cart_id替代
	cart = None
	if 'cart_id' in request.COOKIES:
		try:
			logger.debug('cart_id in cookie:%s' % (request.COOKIES['cart_id']))
			cart = Cart.objects.get(id=request.COOKIES['cart_id'])
			logger.debug('cart exist')
		except:
			logger.debug('cart not exist')
			cart = None
	
	mycart = None
	try:
		mycart = Cart.objects.get(user=request.user)
		logger.debug('mycart exist')
	except:
		logger.debug('mycart not exist')
		mycart = None
	
	if cart == None and mycart == None:
		logger.debug('Create new mycart')
		mycart = Cart.objects.create(user=request.user)
		return mycart
	elif cart == None and mycart != None:
		logger.debug('use the exist mycart')
		return mycart
	elif cart != None and mycart == None:
		logger.debug('use the cart')
		cart.user = request.user
		cart.save()
		return cart
	else:
		#两个购物车都不为空，则要合并
		if cart.id == mycart.id:
			logger.debug('cart is the mycart!')
			return mycart
		else:
			logger.debug('merge')
			for p in cart.cart_products.all():
				has_p = False
				for mp in mycart.cart_products.all():
					if mp.product == p.product and mp.product_attribute == p.product_attribute:
						mp.quantity = mp.quantity + p.quantity
						mp.save()
						p.delete()
						has_p = True
						break;	
				if has_p == False:
					p.cart = mycart
					p.save()
			cart.delete()
			return mycart
			
def logout(request):
	auth.logout(request)
	return redirect(reverse('myuser_login'))
	
def admin_logout(request):
	auth.logout(request)
	return redirect(reverse('admin_index_view'))

	
def forget_password(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Forget Password'
	ctx = add_captcha(ctx) #添加验证码
	if request.method == 'GET':
		ctx['form_display'] = ''
		ctx['success_display'] = 'display:none;'
		return render(request,System_Config.get_template_name() + '/forget_password.html',ctx)
	else:
		form = captcha_form(request.POST) # 获取Post表单数据
		if form.is_valid():
			ctx['form_display'] = 'display:none;'
			ctx.update(csrf(request))
			s_uuid = str(uuid.uuid4())
			reset_password = Reset_Password.objects.create(email=request.POST['email'],validate_code=s_uuid,apply_time=datetime.datetime.now(),expirt_time=(datetime.datetime.now() + datetime.timedelta(hours=24)),is_active=True)
			
			#触发用户申请重置密码的事件
			signals.user_password_modify_applied.send(sender='MyUser',reset_password=reset_password)
			
			#mail_ctx = {}
			#mail_ctx['reset_url'] =  System_Config.get_base_url() + "/user/reset-password?email=" + reset_password.email + "&validate_code=" + reset_password.validate_code
			#my_send_mail(useage='reset_password',ctx=mail_ctx,send_to=reset_password.email,title=_('You are resetting you password in %(site_name)s .') % {'site_name':System_Config.objects.get(name='site_name').val})
			ctx['apply_message'] = _('If there is an account associated with %(email_address)s you will receive an email with a link to reset your password.') % {'email_address':reset_password.email}
			ctx['success_display'] = ''
		else:
			ctx['apply_message'] = _('Please check your verify code.')
		return render(request,System_Config.get_template_name() + '/forget_password.html',ctx)

def reset_password(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Reset Password'
	if request.method == 'GET':
		ctx['success_display'] = 'display:none;'
		ctx['form_display'] = ''
		try:
			#日期大小与比较要用 "日期字段名__gt=" 表示大于
			reset_password = Reset_Password.objects.filter(expirt_time__gt=datetime.datetime.now()).get(email=request.GET['email'],validate_code=request.GET['validate_code'],is_active=True)
			ctx['email'] = reset_password.email
			ctx['validate_code'] = reset_password.validate_code
			return render(request,System_Config.get_template_name() + '/reset_password.html',ctx)
		except:
			raise Http404
			#ctx['form_display'] = 'none'
			#ctx['reset_message'] = _('Can not find the password reset apply request.')
	else:
		try:
			reset_password = Reset_Password.objects.filter(expirt_time__gt=datetime.datetime.now()).get(email=request.POST['email'],validate_code=request.POST['validate_code'],is_active=True)
			myuser = MyUser.objects.get(email=reset_password.email)
			myuser.set_password(request.POST['password'])
			reset_password.is_active = False
			reset_password.save()
			myuser.save()
			
			#触发用户重置密码成功的事件
			signals.user_password_modify_success.send(sender='MyUser',user=myuser)
			
			ctx['success_display'] = ''
			ctx['form_display'] = 'display:none;'
			ctx['reset_message'] = _('The password has been reseted.')
		except:
			ctx['success_display'] = ''
			ctx['form_display'] = 'display:none;'
			ctx['reset_message'] = _('Opration faild.')		
		return render(request,System_Config.get_template_name() + '/reset_password.html',ctx)
		
@login_required
@transaction.atomic()
def address(request,method,id=''):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Address Book'
	result_dict = {}
	result = False
	message = 'System Error'
	if request.method == 'POST':
		address_id = request.POST.get('address_id','')
		logger.debug('The address id is %s.' % (address_id))
		#用途的拼装方法
		useage = request.POST['first_name'] + ' ' + request.POST['last_name'] + '@' + request.POST['city']
		
		#20160525,倪肖勇加入地址数量控制,有一个系统参数 common_user_address_limit,用来控制普通用户的地址数量，如果参数没有设置，默认5条
		address_count = Address.objects.filter(user=request.user).count()
		logger.debug('The address count of this user is:%s' % (address_count))
		limit = 5
		try:
			limit = int(System_Config.objects.get('common_user_address_limit'))
		except:
			logger.info('common_user_address_limit is not setted. use default value 5.')
		can_add = (True if limit > address_count else False)
		logger.debug('Address can add ? %s' % (can_add))
		
		if method == 'add' or method == 'modify':
			if not address_id:
				if can_add:
					address = Address.objects.create(user=request.user)
				else:
					message = _('Only less than %(address_limit)s addresses will be allowed.') % {'address_limit':limit}
					result = False
					result_dict['success'] = result
					result_dict['message'] = message
					return JsonResponse(result_dict)
			else:
				try:
					address = Address.objects.get(user=request.user,id=address_id)
				except Exception as err:
					logger.debug('Can not find address which address_id is %s and belongs to %s .' %(address_id,request.user.email))
					return JsonResponse(result_dict)				
			form = address_form(request.POST,instance=address)
			if form.is_valid():
				address.useage = useage
				address.save()				
				result = True
				message=_('Address successfully saved.')
			else:
				logger.error('address parameter error.' + str(request.POST))
		elif method == 'del':
			logger.debug('TDDO: Delete address')
		else:
			pass
	else:
		#ctx['form'] = address_form()
		if method == 'modify':
			try:
				address = Address.objects.get(id=id,user=request.user)
				ctx['address'] = address
				ctx['title'] = 'Modify Address'
				logger.debug('first_name:' + address.first_name)
			except Exception as err:
				logger.error("Can not find the address which id is %s" % id)
				raise Http404
		elif method == 'add':
			ctx['title'] = 'Add New Address'
		elif method == 'delete':
			address = Address.objects.get(id=id,user=request.user)
			address.delete()
			return redirect('/user/address/show/')
		elif method == 'default':
			address_list = Address.objects.filter(user=request.user)
			for address in address_list:
				logger.debug('id:%s' % (id))
				logger.debug('address_id:%s' % (address.id))
				if address.id == int(id):
					address.is_default = True
					address.save()
				else:
					address.is_default = False
					address.save()
			return redirect('/user/address/show/')
		else:
			raise Http404
		return render(request,System_Config.get_template_name() + '/address_detail.html',ctx)
	
	result_dict['success'] = result
	result_dict['message'] = message
	ret_add = {}
	ret_add['useage'] = address.useage
	ret_add['id'] = address.id
	result_dict['address'] = ret_add
	return JsonResponse(result_dict)

@login_required
def address_list(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Address Book'
	if request.method=='GET':
		myuser = request.user
		address_list = Address.objects.filter(user=myuser)
		ctx['address_list'] = address_list
		return render(request,System_Config.get_template_name() + '/address.html',ctx)
	else:
		raise Http404
	
#@login_required
def address_detail(request,address_id):
	ctx = {}
	result_dict = {}
	result = False
	if request.method=='GET':
		try:
			address = Address.objects.get(user=request.user,id=address_id)
			from shopcart.serializer import serializer
			serialized_address = serializer(address,datetime_format='string',output_type='dict')
			#serialized_address = serialized_address.replace('\n','').replace('\\"','"')
			logger.debug(serialized_address)
			result_dict['address'] = serialized_address
			result = True
		except Exception as err:
			logger.error('Can not find the address which id is %s and user is %s .' % (address_id,request.user.email))
			logger.error(str(err))
	result_dict['success'] = result
	#return HttpResponse(serializer(result,datetime_format='string',output_type='json'))
	return JsonResponse(result_dict)

			
			
			
			
			
			
			
			
			
			
			