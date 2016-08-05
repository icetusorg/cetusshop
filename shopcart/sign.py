import time
import random
import string
import hashlib
import logging
logger = logging.getLogger('icetus.shopcart')

class Sign:
	def __init__(self, jsapi_ticket, url):
		self.ret = {
			'nonceStr': self.__create_nonce_str(),
			'jsapi_ticket': jsapi_ticket,
			'timestamp': self.__create_timestamp(),
			'url': url
		}

	def __create_nonce_str(self):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

	def __create_timestamp(self):
		return int(time.time())

	def sign(self):
		string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
		logger.debug('string:%s' % (string))
		signature = hashlib.sha1(string.encode('utf8')).hexdigest()
		self.ret['signature'] = signature
		logger.debug('signature:%s' % (signature))
		return self.ret

