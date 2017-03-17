#coding=utf-8
from django.conf import settings 
from django.http import HttpResponseRedirect
import sys
from django.views.debug import technical_500_response
import logging
logger = logging.getLogger('icetus.shopcart')

class MyLoginCheckMiddleware:
	def process_request(self, request):
		#logger.debug('Come into the process_request.')
		myuser = request.user
		if myuser.is_anonymous():
			#匿名用户，不控制
			#path = request.path
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
			
		vars['full_path'] = request.get_full_path()
		vars['path'] = request.path
		response.context_data['customize_var'] = vars
		#logger.debug('customize_var:%s' % vars)
		
		
		from shopcart.utils import get_system_parameters
		response.context_data['system_para'] = get_system_parameters()
		
		#logger.debug("Look up: %s" % response.context_data['customize_var'])
		return response
		
	#对超级用户，可以看到报错信息	
	def process_exception(self, request, exception):
		if request.user.is_superuser:
			return technical_500_response(request, *sys.exc_info())	