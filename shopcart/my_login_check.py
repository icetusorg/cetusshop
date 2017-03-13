#coding=utf-8
from django.conf import settings 
from django.http import HttpResponseRedirect
import logging
logger = logging.getLogger('icetus.shopcart')

class MyLoginCheckMiddleware:
	def process_request(self, request):
		logger.debug('Come into the process_request.')
		myuser = request.user
		if myuser.is_anonymous():
			#匿名用户，不控制
			pass
		else:
			logger.debug('%s' % myuser)
			path = request.path_info.lstrip('/')
			logger.debug('path:%s' % path)
			if not path=='user/login/':
				if myuser.is_active == False:
					logger.info('%s user has been banned. Reject!' % request.user.email)
					from django.contrib import auth
					auth.logout(request)
					return HttpResponseRedirect(settings.LOGIN_URL)
				
