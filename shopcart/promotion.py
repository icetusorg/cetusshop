#coding=utf-8
from django.shortcuts import render
from django.template.loader import render_to_string
from shopcart.models import System_Config,Promotion
import json
from django.http import JsonResponse,Http404,HttpResponse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger('icetus.shopcart')

# Create your views here.
@csrf_exempt
def calculate(request):
	if request.method == 'POST':
		code = request.GET.get('code','')
			
		try:
			promotion = Promotion.objects.get(code=code)
		except:
			result = {}
			result['success'] = False
			result['message'] = 'The promotion code is not valid.'
			return JsonResponse(result)
		
		import importlib
		#装载优惠方法实现类
		module = 'shopcart.promotion_impl.%s' % (promotion.impl_class)
		logger.info('The promotion impl class is [%s] ' %(module))
		try:
			promotion_impl = importlib.import_module(module)
		except Exception as err:
			logger.error('Can not load module:[%s]' % (module))
			raise Http404
		
		return JsonResponse(promotion_impl.calculate(request,promotion)) 


		
