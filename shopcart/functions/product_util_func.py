#coding=utf-8
from django.db import transaction
from django.utils.translation import ugettext as _
import datetime,uuid
from django.core.serializers import serialize,deserialize
from shopcart.utils import url_with_out_slash

import logging
logger = logging.getLogger('icetus.shopcart')

def get_menu_products():
	from shopcart.models import Product
	product_list = Product.objects.filter(is_publish=True)
	return product_list

def get_url(object):
	from shopcart.models import System_Config,Product
	url = url_with_out_slash(System_Config.objects.get(name='base_url').val)
	
	
	if isinstance(object,Product):
		if object.static_file_name == None or object.static_file_name == '':
			#return  url + '/product/' + object.id
			return ('%s/product/%s' % (url,object.id))
		else:
			return ('%s/%s' % (url,object.static_file_name))
			#return url + '/' + object.static_file_name
	else:
		return '#'