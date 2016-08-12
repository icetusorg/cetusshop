#coding=utf-8
from django.shortcuts import render
from django.template.loader import render_to_string
from shopcart.models import System_Config,Category
from shopcart.utils import System_Para,my_pagination,get_system_parameters
import json,os
from django.http import JsonResponse
from django.http import Http404
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
import logging
logger = logging.getLogger('icetus.shopcart')

def category_list(request):
	top_category_list = Category.objects.filter(parent=None)
	
	for cat in top_category_list:
		deal_category(cat)
	
	ctx = {}
	ctx['categorys'] = top_category_list
	logger.debug('Top Categorys : %s' % top_category_list)
	return JsonResponse({'success':'OK'})
	
	
def deal_category(category):
	logger.debug('I am %s' % category)
	for cat in category.childrens.all():
		logger.debug('Has children.')
		deal_category(cat)