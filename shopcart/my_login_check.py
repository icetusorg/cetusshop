#coding=utf-8
from django.conf import settings 
from django.http import HttpResponseRedirect
import logging
logger = logging.getLogger('icetus.shopcart')

class MyLoginCheckMiddleware:
	def process_request(self, request):
		#logger.debug('Come into the process_request.')
		myuser = request.user
		if myuser.is_anonymous():
			#匿名用户，不控制
			pass
		else:
			#logger.debug('%s' % myuser)
			path = request.path_info.lstrip('/')
			#logger.debug('path:%s' % path)
			if not path=='user/login/':
				if myuser.is_active == False:
					#logger.info('%s user has been banned. Reject!' % request.user.email)
					from django.contrib import auth
					auth.logout(request)
					return HttpResponseRedirect(settings.LOGIN_URL)
				
	def process_template_response(self,request,response):
		logger.debug('Come into the process_template_response')
		logger.debug('Add custmizeVar into context_data...')
		from shopcart.models import CustomizeVar
		vars = {}
		for var in CustomizeVar.objects.all():
			vars[var.name] = var.value
			
		response.context_data['customize_var'] = vars
		
		logger.debug("Look up: %s" % response.context_data['customize_var'])
		return response