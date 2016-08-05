# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.http import JsonResponse,QueryDict
from shopcart.models import System_Config,Product,Product_Images,Category,MyUser,Email,Reset_Password,Address,Product_Attribute,Attribute_Group,Attribute,Article,Express,ExpressType
from shopcart.utils import my_send_mail,get_serial_number
from django.db import transaction
from django.utils.translation import ugettext as _
import datetime
import requests
from shopcart.utils import get_system_parameters
from shopcart.functions.product_util_func import get_menu_products
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('imycart.shopcart')


def contact_page(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Contact us'
	
	return render(request,System_Config.get_template_name() + '/contact.html',ctx)

def url_dispatch(request,url):
	logger.debug('Url to dispatch:' + url)
	
	from shopcart.models import Product,Category,Article
	#优先级 1 ：解析商品路径
	try:
		product = Product.objects.get(static_file_name=url)
		#mvc解析
		from shopcart.product import detail
		return detail(request,product.id)
		
		#301跳转模式
		#return redirect('/product/'+str(product.id))
	except Exception as err:
		logger.error('Can not find url [%s] in products.' % (url))
	
	
	#优先级 2 ：解析分类路径
	#暂未实现
	
	#优先级 3 ：解析文章路径
	try:
		article = Article.objects.get(static_file_name=url)
		from shopcart.article import detail
		return detail(request,article.id)
	except Exception as err:
		logger.error('Can not find url [%s] in artilces.' % (url))
		
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
		raise Http404
		
		
	result = initial_system.init_db()
	return HttpResponse(result)