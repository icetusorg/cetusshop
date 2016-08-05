#coding=utf-8
from django.db import transaction
from django.utils.translation import ugettext as _
import datetime,uuid
from django.core.serializers import serialize,deserialize

import logging
logger = logging.getLogger('icetus.shopcart')

def get_url(object):
	from shopcart.models import System_Config,Article
	url = System_Config.objects.get(name='base_url').val
	
	if isinstance(object,Article):
		if object.static_file_name == None or object.static_file_name == '':
			return  url + '/article/' + object.id
		else:
			return url + '/' + object.static_file_name
	else:
		return '#'