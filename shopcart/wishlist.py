#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Wish,Product,System_Config
from django.core.context_processors import csrf
from django.http import HttpResponse,JsonResponse
import json,uuid
from django.db import transaction
from shopcart.utils import System_Para,my_pagination,get_system_parameters
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from shopcart.functions.product_util_func import get_menu_products

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

def add_to_wishlist(request):
	ctx = {}
	ctx.update(csrf(request))
	result_dict = {}
	
	if request.method =='POST':
		product_to_be_add = json.loads((request.body).decode())		
		
		if request.user.is_authenticated():
			product = Product.objects.get(id=product_to_be_add['product_id'])
			wish,created = Wish.objects.get_or_create(user=request.user,product=product)
			result_dict['success'] = True
			result_dict['message'] = _('Collected successfully and you can check in your lovely wishlist！')
		else:
			#还没登陆
			result_dict['success'] = False
			result_dict['message'] = 'needLogin'
			result_dict['next'] = '/product/%s' % (product_to_be_add['product_id'])
			
		
		return JsonResponse(result_dict)

@login_required()
def view_wishlist(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'My Wishlist'
	if request.method =='GET':
		wish_list = Wish.objects.filter(user=request.user)
		
		try:
			page_size = int(System_Config.objects.get(name='wish_list_page_size').val)
		except:
			logger.info('The system parameter [wish_list_page_size] is not setted,use the default value 5.')
			page_size = 5
		
		wish_list, page_range = my_pagination(request, wish_list,display_amount=page_size)
		ctx['wish_list'] = wish_list
		ctx['page_range'] = page_range
		return TemplateResponse(request,System_Config.get_template_name() + '/wish_list.html',ctx)
		
@login_required()
def remove_from_wishlist(request):
	ctx = {}
	ctx.update(csrf(request))
	result_dict = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	if request.method =='POST':
		wish_to_be_delete = json.loads((request.body).decode())	
		try:
			wish = Wish.objects.get(id=wish_to_be_delete['id'],user=request.user)
			wish.delete()
		except:
			pass
		
		result_dict['success'] = True
		result_dict['message'] = _('Opration successful.')	
		return JsonResponse(result_dict)