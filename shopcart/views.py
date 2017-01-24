# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.http import JsonResponse,QueryDict
from shopcart.models import System_Config,Product,Product_Images,Category,MyUser,Email,Reset_Password,Address,Product_Attribute,Attribute_Group,Attribute,Article,Express,ExpressType
from shopcart.utils import my_send_mail,get_serial_number,customize_tdk
from django.db import transaction
from django.utils.translation import ugettext as _
import datetime
import requests
from shopcart.utils import get_system_parameters
from shopcart.functions.product_util_func import get_menu_products
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


def contact_page(request,tdk=None):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Contact us'
	
	customize_tdk(ctx,tdk)
	
	return render(request,System_Config.get_template_name() + '/contact.html',ctx)

def url_dispatch(request,url):
	logger.debug('Url to dispatch:' + url)
	
	from shopcart.models import Product,Category,Article,CustomizeURL
	#优先级 1 ：解析商品路径
	try:
		product = Product.objects.get(static_file_name=url)
		#mvc解析
		from shopcart.product import detail
		return detail(request,product.id)
		
		#301跳转模式
		#return redirect('/product/'+str(product.id))
	except Exception as err:
		logger.error('Can not find url [%s] in products. Error message is %s' % (url,err))
	
	
	#优先级 2 ：解析分类路径
	#暂未实现
	try:
		cate = Category.objects.get(static_file_name=url)
		#mvc解析
		from shopcart.product import category
		return category(request,cate.id)
		
	except Exception as err:
		logger.error('Can not find url [%s] in Category.Error message is %s' % (url,err))
	
	
	#优先级 3 ：解析文章路径
	try:
		article = Article.objects.get(static_file_name=url)
		from shopcart.article import detail
		return detail(request,article.id)
	except Exception as err:
		logger.error('Can not find url [%s] in artilces.Error message is %s' % (url,err))
			
	#优先级 4 ： 自定义URL
	try:
		cust = CustomizeURL.objects.get(url = url)
		if cust.type == 'MVC':
			logger.info('CustomizeURL module is [%s],function is [%s].' % (cust.module,cust.function))
			import importlib
			module = importlib.import_module(cust.module)
			logger.debug('Module : [%s]' % module)
			function =  getattr(module,cust.function)
			logger.info('Function is [%s].' % function)
			
			tdk = None
			if cust.is_customize_tdk:
				tdk = {}
				tdk['page_title'] = cust.page_name
				tdk['keywords'] = cust.keywords
				tdk['short_desc'] = cust.short_desc
			
			return function(request,tdk)
		else:	
			return redirect(cust.target_url)
	except Exception as err:
		logger.error('Can not find url [%s] in customizeURL.Error message is %s' % (url,err))
		
	raise Http404
	
	

def init_database(request):
	import importlib
	#装载初始化方法文件
	module = 'shopcart.%s' % ('initial_system')
	logger.info('The init impl class is [%s] ' %(module))
	try:
		initial_system = importlib.import_module(module)
	except Exception as err:
		logger.error('Can not load module:[%s]' % (module))
		logger.error('Error Message: %s' % err)
		raise Http404
		
		
	result = initial_system.init_db()
	return HttpResponse(result)