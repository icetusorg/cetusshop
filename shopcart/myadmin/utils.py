#coding=utf-8
from shopcart.models import Article,System_Config

import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

NO_PERMISSION_PAGE = '/admin/no-permission/'

def is_permitted(permission_list,user):
	pass
	