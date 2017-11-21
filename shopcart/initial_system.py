# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.http import JsonResponse,QueryDict
from shopcart.models import System_Config,Product,Product_Images,Category,MyUser,Email,Reset_Password,Address,Product_Attribute,Attribute_Group,Attribute,Article,Express,ExpressType,Order,CustomizeURL,OAuthSite
from django.db import transaction
from django.utils.translation import ugettext as _
import datetime
import requests
from shopcart.utils import get_system_parameters
import logging
logger = logging.getLogger('icetus.shopcart')

def init_permissions():
	from django.contrib.auth.models import Permission
	from django.contrib.contenttypes.models import ContentType
	#先把自动产生的那些权限项给删了
	Permission.objects.all().delete()
	
	#订单类权限
	content_type = ContentType.objects.get_for_model(Order)
	permission = Permission.objects.create(codename='can_list_order',name='订单列表',content_type=content_type)
	permission = Permission.objects.create(codename='can_delete_order',name='订单删除',content_type=content_type)
	permission = Permission.objects.create(codename='can_edit_order',name='订单编辑',content_type=content_type)
	permission = Permission.objects.create(codename='can_pay_order',name='订单支付',content_type=content_type)
	permission = Permission.objects.create(codename='can_remark_list_order',name='订单备注列表',content_type=content_type)
	permission = Permission.objects.create(codename='can_remark_order',name='订单备注',content_type=content_type)
	permission = Permission.objects.create(codename='can_repay_order',name='订单退款',content_type=content_type)
	permission = Permission.objects.create(codename='can_return_order',name='订单退货',content_type=content_type)
	permission = Permission.objects.create(codename='can_ship_order',name='订单发货',content_type=content_type)
	permission = Permission.objects.create(codename='can_stock_up_order',name='订单备货',content_type=content_type)
	

def init_categorys():
	cat = Category(code='whole',name='所有品类')
	cat.save()
	

def init_expresses():
	express_type_fastest = ExpressType.objects.create(name='Fastest',price_fixed=10.00,price_per_kilogram=0)
	express_type_faster = ExpressType.objects.create(name='Faster',price_fixed=8.00,price_per_kilogram=0)
	express_type_normal = ExpressType.objects.create(name='Normal',price_fixed=6.00,price_per_kilogram=0)
	
	express = Express.objects.create(name='Fedx',price_fixed=0.00,price_per_kilogram=0)
	express.express_type.add(express_type_fastest)
	express.express_type.add(express_type_faster)
	express.save()
	
	express = Express.objects.create(name='DHL',price_fixed=0.00,price_per_kilogram=0)
	express.express_type.add(express_type_faster)
	express.save()
	
	express = Express.objects.create(name='EMS',price_fixed=0.00,price_per_kilogram=0)
	express.express_type.add(express_type_normal)
	express.save()

def init_system_configs():
	sys_con = System_Config.objects.create(name='template_name',val='cassie')
	sys_con = System_Config.objects.create(name='site_name',val='鲸鱼座商城')
	sys_con = System_Config.objects.create(name='default_welcome_message',val='Hi，欢迎来鲸鱼座商城')
	sys_con = System_Config.objects.create(name='logo_image',val='http://www.icetuscom/images/logo.png')
	sys_con = System_Config.objects.create(name='base_url',val='http://localhost:8000/')
	sys_con = System_Config.objects.create(name='paypal_account',val='demo@icetus.com')
	sys_con = System_Config.objects.create(name='default_currency',val='USD')
	sys_con = System_Config.objects.create(name='paypal_env',val='sandbox')
	
	sys_con = System_Config.objects.create(name='copyright',val='Copyright © cassiecomb.com All Rights Reserved. Designed by iCetus')
	sys_con = System_Config.objects.create(name='service_email',val='info@cassiecomb.com')
	sys_con = System_Config.objects.create(name='contact_address',val='4578 MARMORA ROAD,GLASGOW D04 89 GR')
	sys_con = System_Config.objects.create(name='thumb_width',val='128')
	
	sys_con = System_Config.objects.create(name='hot_line',val='(+86)186 18 18 18')
	sys_con = System_Config.objects.create(name='office_phone',val='(+86)86688668')
	
	sys_con = System_Config.objects.create(name='workday',val='Mon - Sun / 9:00AM - 8:00PM(BeiJing Time)')
	
	sys_con = System_Config.objects.create(name='product_page_size',val=12)
	sys_con = System_Config.objects.create(name='common_user_address_limit',val=4)
	sys_con = System_Config.objects.create(name='order_list_page_size',val=10)
	sys_con = System_Config.objects.create(name='blog_list_page_size',val=12)
	
	sys_con = System_Config.objects.create(name='admin_template_name',val='default')
	sys_con = System_Config.objects.create(name='admin_order_list_page_size',val=12)
	
	sys_con = System_Config.objects.create(name='email_template_name',val='default')
	
	
	

def init_attributes():
	ag_Color = Attribute_Group.objects.create(name='Color',group_type='image',code='Color')
	
	ab_Color_RED =  Attribute.objects.create(name='RED',group=ag_Color,position=0,thumb='http://aws.imycart.com/media/attribute/Color/RED.jpg')
	ab_Color_GREEN =  Attribute.objects.create(name='GREEN',group=ag_Color,position=1,thumb='http://aws.imycart.com/media/attribute/Color/GREEN.jpg')
	ab_Color_BLUE =  Attribute.objects.create(name='BLUE',group=ag_Color,position=2,thumb='http://aws.imycart.com/media/attribute/Color/BLUE.jpg')
	
def init_products():
	product_brush = Product(item_number='BRUSH001',name='Top-quality no tangle 360° hair brush ball',quantity=500,market_price=14.99,price=9.99,description='',short_desc='Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.',static_file_name='',is_publish=True)
	product_brush.description = '<p>This kind hair brush can do many different workmanship, so you can choose what you like. Because its personalized shape and design make it become the most popular hair brush in the world, especially in North America. It is the hottest seller and many surprises wait for you.</p><div>1. Portable, for woman can put it in bag.</div><div>2. The different length of tooth can massage the different surface of hair so can protect your hair from damage and loss.</div><div>3. Can do many cover designs, like figure, scenery and animation.</div><div>4. The unique cone shaped plastic bristles work to separate the hair sideways instead of down, gently unraveling even the toughest tangles</div><div>5. Great for Extensions</div><div>6. Our brush also encourages hair growth. The bristles massage the scalp, which stimulates the capillaries, increasing blood circulation, oxygen and nutrients to the hair follicle.</div>'
	product_brush.save()
	product_brush.thumb = 'http://aws.imycart.com/media/product/18/003fee96-1d8b-11e6-b3b0-0ab91c1e4bd1-thumb.jpg'
	product_brush.image = 'http://aws.imycart.com/media/product/18/003fee96-1d8b-11e6-b3b0-0ab91c1e4bd1.jpg'
	product_brush.save()
	
	image_red = Product_Images()
	image_red.product = product_brush
	image_red.thumb = 'http://aws.imycart.com/media/product/18/fce1b180-1d8a-11e6-b3b0-0ab91c1e4bd1-thumb.jpg'
	image_red.image = 'http://aws.imycart.com/media/product/18/fce1b180-1d8a-11e6-b3b0-0ab91c1e4bd1.jpg'
	image_red.save()
	
	image_black = Product_Images()
	image_black.product = product_brush
	image_black.thumb = 'http://aws.imycart.com/media/product/18/003fee96-1d8b-11e6-b3b0-0ab91c1e4bd1-thumb.jpg'
	image_black.image = 'http://aws.imycart.com/media/product/18/003fee96-1d8b-11e6-b3b0-0ab91c1e4bd1.jpg'
	image_black.save()
	
	pa_red = Product_Attribute.objects.create(product=product_brush,sub_item_number=1,quantity=500,price_adjusment=-0.99,image=image_red)
	ab_Color_RED = Attribute.objects.get(name='RED')
	pa_red.attribute.add(ab_Color_RED)
	pa_red.name = 'RED'
	pa_red.min_order_quantity = 10
	pa_red.save()
	
	pa_green = Product_Attribute.objects.create(product=product_brush,sub_item_number=2,quantity=420,price_adjusment=1.99,image=image_black)
	ab_Color_GREEN = Attribute.objects.get(name='GREEN')
	pa_green.attribute.add(ab_Color_GREEN)
	pa_green.name = 'GREEN'
	pa_green.min_order_quantity = 0
	pa_green.save()
	
	pa_blue = Product_Attribute.objects.create(product=product_brush,sub_item_number=3,quantity=360,price_adjusment=0,image=image_red)
	ab_Color_BLUE = Attribute.objects.get(name='BLUE')
	pa_blue.attribute.add(ab_Color_BLUE)
	pa_blue.name = 'BLUE'
	pa_blue.min_order_quantity = 5
	pa_blue.save()

def init_users():
	myuser = MyUser.objects.create_superuser(email='super@icetus.com',password='icetus',username='Super',gender='1')
	myuser.is_superuser = True
	myuser.is_staff = True
	myuser.save()
	
def init_email():
	email_address = 'support@icetus.com'
	smtp_host = 'smtp.exmail.qq.com'
	username = 'support@icetus.com'
	password = 'iCetus2016'
	
	email = Email.objects.create(useage='user_registration_success',email_address=email_address,smtp_host=smtp_host,username=username,password=password,template='default',template_file='user_registration_success.html')
	emial_sys = System_Config.objects.create(name='user_registration_success_send_mail',val='true')
	
	email = Email.objects.create(useage='user_password_modify_applied',email_address=email_address,smtp_host=smtp_host,username=username,password=password,template='default',template_file='user_password_modify_applied.html')
	emial_sys = System_Config.objects.create(name='user_password_modify_applied_send_mail',val='true')
	
	email = Email.objects.create(useage='user_password_modify_success',email_address=email_address,smtp_host=smtp_host,username=username,password=password,template='default',template_file='user_password_modify_success.html')
	emial_sys = System_Config.objects.create(name='user_password_modify_success_send_mail',val='true')
	
	email = Email.objects.create(useage='order_was_payed',email_address=email_address,smtp_host=smtp_host,username=username,password=password,template='default',template_file='order_was_payed.html')
	emial_sys = System_Config.objects.create(name='order_was_payed_send_mail',val='true')

def init_cust_url():
	cust_url = CustomizeURL.objects.create(name='login',url='index-login.html',target_url='/user/login/',module='shopcart.myuser',function='login',type='MVC',is_customize_tdk='0',page_name='Login Page',keywords='Keywords of login page',short_desc='Short desc of login page')
	
	cust_url = CustomizeURL.objects.create(name='index',url='index.html',target_url='/',module='shopcart.index',function='view_index',type='MVC',is_customize_tdk='1',page_name='Index Page',keywords='Keywords of index page',short_desc='Short desc of index page')
	
	cust_url = CustomizeURL.objects.create(name='blog',url='blog-list.html',target_url='/blog/',module='shopcart.article',function='view_blog_list_with_tdk',type='MVC',is_customize_tdk='1',page_name='Blog Page',keywords='Keywords of blog page',short_desc='Short desc of blog page')
	
	cust_url = CustomizeURL.objects.create(name='contact_us',url='Contact-us.html',target_url='/contact/show/',module='shopcart.views',function='contact_page',type='MVC',is_customize_tdk='1',page_name='Contact us Page',keywords='Keywords of contact us page',short_desc='Short desc of contact us page')

	
def init_oauth():
	pass
	#oauth_site = OAuthSite.objects.create(name='wechat',impl_class='shopcart.oauth.sites.wechat.Wechat',redirect_uri='',client_id='',client_secret='',scope_login='',scope_info='')


	
@transaction.atomic()
def init_db():
	try:
		flag = System_Config.objects.get(name='inited_flag').val
		logger.info('Init flag has been setted.')
		return '数据已经初始化，不可重复执行。'
	except:
		System_Config.objects.create(name='inited_flag',val='inited')
		pass
	init_permissions()
	init_categorys()
	init_expresses()
	init_system_configs()
	init_attributes()
	init_products()
	init_users()
	init_email()
	return '成功'