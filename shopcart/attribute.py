#coding=utf-8
from django.shortcuts import render
from django.template.loader import render_to_string
from shopcart.models import System_Config,Attribute,Attribute_Group,Product_Attribute
from shopcart.utils import my_pagination,get_system_parameters
import json,os
from django.http import JsonResponse
from django.http import Http404
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
import logging
logger = logging.getLogger('icetus.shopcart')

def get_group_info(request,id=None):
	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = ''
	result_dict['data'] = {}
	
	try:
		group = Attribute_Group.objects.get(id=id)
	except Exception as err:
		logger.error('Can not find attribute_group which id is %s.' % id)
		result_dict['message'] = _('找不到属性组信息，可能已经被删除了，请重试。')
		return JsonResponse(result_dict)
	
	
	from shopcart.serializer import serializer
	
	attributes = {} 
	for att in group.attributes.all():
		logger.debug("att:%s"%att.name)
		serialized_attr = serializer(att,datetime_format='string',output_type='dict')
		attributes[att.code] = serialized_attr

	result_dict['data']['items'] = attributes
	serialized_group = serializer(group,datetime_format='string',output_type='dict')	
		
	result_dict['data']['group'] = serialized_group	
	result_dict['success'] = True
	return JsonResponse(result_dict)
