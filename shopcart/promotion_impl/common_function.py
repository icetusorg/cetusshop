#coding=utf-8
import logging
logger = logging.getLogger('icetus.shopcart')

def is_valid(promotion):
	if not promotion.is_valid:
		logger.info('The promotion code has been used.')
		return False
	
	import datetime
	now = datetime.datetime.now()
	
	if now.timestamp() > promotion.valid_date_begin.timestamp() and now.timestamp() < promotion.valid_date_end.timestamp():
		return True
	else:
		logger.info('Promotion code is not valid,now:[%s],valid_date_begin:[%s],valid_date_end:[%s]' % (now.timestamp(),promotion.valid_date_begin.timestamp(),promotion.valid_date_end.timestamp()))
		return False
	
		
