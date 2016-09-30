#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import System_Config
from shopcart.utils import get_system_parameters
from django.http import HttpResponse


from django.contrib.admin.views.decorators import staff_member_required
import logging
logger = logging.getLogger('icetus.shopcart')

@staff_member_required
def menu_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	return render(request,System_Config.get_template_name('admin') + '/menu.html',ctx)

@staff_member_required	
def view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	if request.method == 'GET':
		return render(request,System_Config.get_template_name('admin') + '/index.html',ctx)
		
@staff_member_required	
def content_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	if request.method == 'GET':
		return render(request,System_Config.get_template_name('admin') + '/index_content.html',ctx)
		
def login(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	if request.method == 'GET':
		return render(request,System_Config.get_template_name('admin') + '/login.html',ctx)
	
def no_permission(request):
	return HttpResponse('您没有相应的权限，请联系管理员分配。')