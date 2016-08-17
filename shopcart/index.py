# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from shopcart.models import System_Config
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse
from shopcart.utils import get_system_parameters
import json
from django.utils.translation import ugettext as _
from shopcart.functions.product_util_func import get_menu_products
from django.http import Http404
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


# Create your views here.
def view_index(request): 
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Home'
	ctx['page_key_words'] = ''
	ctx['page_description'] = ''
	
	try:
		ctx['page_name'] = System_Config.objects.get(name='index_page_title').val
		ctx['page_key_words'] = System_Config.objects.get(name='index_keywords').val
		ctx['page_description'] = System_Config.objects.get(name='index_description').val
	except Exception as err:
		logger.info('The system parameter page_name,page_key_words,page_description maybe has not setted.')
	
	return render(request,System_Config.get_template_name() + '/index.html',ctx)
	
	
#刷新验证码  
def refresh_captcha(request):  
		to_json_response = dict()  
		to_json_response['status'] = 1  
		to_json_response['new_cptch_key'] = CaptchaStore.generate_key()  
		to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])  
		return HttpResponse(json.dumps(to_json_response), content_type='application/json')
