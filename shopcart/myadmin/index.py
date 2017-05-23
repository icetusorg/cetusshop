#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import System_Config,Order
from shopcart.utils import get_system_parameters
from django.template.response import TemplateResponse
from django.http import HttpResponse,JsonResponse


from django.contrib.admin.views.decorators import staff_member_required
import logging
logger = logging.getLogger('icetus.shopcart')

@staff_member_required
def menu_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	return TemplateResponse(request,System_Config.get_template_name('admin') + '/menu.html',ctx)

@staff_member_required	
def view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	if request.method == 'GET':
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/index.html',ctx)
		
def heart(request):
	result = {}
	result['success'] = True
	return JsonResponse(result)
		
@staff_member_required	
def content_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	if request.method == 'GET':
		import datetime
		#start_date = datetime.date(2017, 3, 15)
		#end_date = datetime.date(2017, 3, 16)
		now = datetime.datetime.now()
		start = now - datetime.timedelta(hours=23,minutes=59,seconds=59)
		ctx['order_count_today'] = Order.objects.filter(create_time__gt=start).count()
		ctx['order_not_pay_count_today'] = Order.objects.filter(create_time__gt=start).filter(status=Order.ORDER_STATUS_PLACE_ORDER).count()
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/index_content.html',ctx)
		
def login(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	if request.method == 'GET':
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/login.html',ctx)
	
def no_permission(request):
	return HttpResponse('您没有相应的权限，请联系管理员分配。')