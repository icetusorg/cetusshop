# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from shopcart.models import System_Config,CustomizeURL,ClientMenu,Slider
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse
from shopcart.utils import get_system_parameters,customize_tdk
import json
from django.utils.translation import ugettext as _
from shopcart.functions.product_util_func import get_menu_products
from django.http import Http404
from django.http import HttpResponse,JsonResponse
from django.template.response import TemplateResponse
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


# Create your views here.
def view_index(request,tdk=None): 
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	if not tdk:
		try:
			cust = CustomizeURL.objects.get(name = '首页')
			if cust.is_customize_tdk:
				tdk = {}
				tdk['page_title'] = cust.page_name
				tdk['keywords'] = cust.keywords
				tdk['short_desc'] = cust.short_desc
		except Exception as err:
			tdk = None

	if tdk:
		customize_tdk(ctx,tdk)

	
	return TemplateResponse(request,System_Config.get_template_name() + '/index.html',ctx)
	
	
#刷新验证码  
def refresh_captcha(request):  
		to_json_response = dict()  
		to_json_response['status'] = 1  
		to_json_response['new_cptch_key'] = CaptchaStore.generate_key()  
		to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])  
		return HttpResponse(json.dumps(to_json_response), content_type='application/json')

		
def get_menu(request):
	code = request.GET.get('menu_name','common_header')
	try:
		menu = ClientMenu.objects.get(code=code)
	except Exception as err:
		logger.error('Can not find menu %s. \n Error Message:%s' %(code,err))
		menu = ''
		
	result_dict = {}
	result_dict['success'] = True
	result_dict['data_menu'] = menu.content
	return JsonResponse(result_dict)
	
	
def get_slider_images(request):
	code = request.GET.get('slider_name','')
	try:
		slider = Slider.objects.get(code=code)
	except Exception as err:
		logger.error('Can not find slider %s. \n Error Message:%s' %(code,err))
		slider = None
	
	result_dict = {}
	result_dict['success'] = True
	image_list = []
	for img in slider.get_image_list():
		image = {}
		image['image'] = img.image
		image['href'] = img.href
		image['alt'] = img.alt_value
		image_list.append(image)
	result_dict['image_list'] = image_list
	return JsonResponse(result_dict)
		
		
		
		