#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.views.decorators.csrf import csrf_exempt
from shopcart.models import MyUser
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse
#引入JsonResponse，用来处理Json请求
from django.http import JsonResponse
from django.utils.translation import ugettext as _
import json
from captcha.models import CaptchaStore
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')
# Create your views here.

@csrf_exempt
def ajax_validate_user(request,exits):
	result_dict = {}

	myuser = None
	if 'value' in request.GET:
		query_str = request.GET['value'].lower()
	elif 'email' in request.POST:
		query_str = request.POST['email'].lower()
		
	try:
		myuser = MyUser.objects.get(email=query_str)
	except:
		pass
	
	if myuser == None:
		#myuser是None，说明用户不存在
		if exits == 'hope-not-exits':
			result_dict['valid'] = True
			result_dict['value'] = query_str
			result_dict['message'] = _('The email has been registered!')
		else:
			result_dict['valid'] = False
			result_dict['value'] = query_str
			result_dict['message'] = _('The email has not been registered!')
	else:
		#myuser是None，说明用户已经存在
		if exits == 'hope-not-exits':
			result_dict['valid'] = False
			result_dict['value'] = query_str
			result_dict['message'] = _('The email has been registered!')
		else:
			result_dict['valid'] = True
			result_dict['value'] = query_str
			result_dict['message'] = _('The email has not been registered!')

	return JsonResponse(result_dict)
	
def ajax_validate_captcha(request):
	if  request.is_ajax():
		cs = CaptchaStore.objects.filter(response=request.GET['response'],hashkey=request.GET['hashkey'])
		result_dict = {}
		if cs:
			result_dict['success'] = True
			result_dict['message'] = _('Varify code is correct.')
			return JsonResponse(result_dict)
		else:
			result_dict['success'] = False
			result_dict['message'] = _('Varify code is not correct.')
			return JsonResponse(result_dict)