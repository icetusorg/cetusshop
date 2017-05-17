# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('icetus.shopcart')

def import_oauth_class(m):
	logger.debug('m:%s' % m)
	m = m.split('.')
	c = m.pop(-1)
	logger.debug('m:%s,c:%s' % (m,c))
	module = __import__('.'.join(m), fromlist=[c])
	return getattr(module, c)
