#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import ExpressType,Express,System_Config
from shopcart.utils import System_Para,my_pagination,get_serial_number,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart.forms import express_form,express_type_form
import logging
logger = logging.getLogger('icetus.shopcart')

	
@staff_member_required
@transaction.atomic()	
def type_list_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '配送方式管理'
	
	if request.method == 'GET':
		express_type_list = ExpressType.objects.filter(is_delete=False)
		
		express_type_list, page_range = my_pagination(request=request, queryset=express_type_list,display_amount=15)
		ctx['page_range'] = page_range
		ctx['item_count'] = ExpressType.objects.all().count()
		ctx['page_size'] = 15
		
		
		ctx['express_type_list'] = express_type_list
		return render(request,System_Config.get_template_name('admin') + '/delivery_type_list.html',ctx)
	else:
		raise Http404
	

@staff_member_required
@transaction.atomic()	
def type_edit(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '配送方式管理'
	
	if request.method == 'GET':
		try:
			id = request.GET.get('id','')
			express_type = ExpressType.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find express_type which id is [%s].\n Error Message: %s' % (id,err))
			express_type = None
		
		ctx['express_type'] = express_type
		ctx['express_list'] = Express.objects.filter(is_delete=False)
		return render(request,System_Config.get_template_name('admin') + '/delivery_type_detail.html',ctx)
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '配送方式信息保存失败'
		
		express_type = None
		
		try:
			id = request.POST.get('id','')
			express_type = ExpressType.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find express_type which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			
		if express_type:
			form = express_type_form(request.POST,instance=express_type)
		else:
			form = express_type_form(request.POST)
			
		if form.is_valid():
			express_type = form.save()

			express_id_list = request.POST.getlist('express')
			express_list = Express.objects.filter(id__in=express_id_list)
			express_type.expresses = express_list
			express_type.save()	
			
			result['success'] = True
			result['message'] = '配送方式信息保存成功'
			result['express_type_id'] = express_type.id
		
		return JsonResponse(result)		
	else:
		raise Http404	
		
		
@staff_member_required
@transaction.atomic()	
def type_delete(request,id):
	result = {}
	result['success'] = False
	result['message'] = ''
	
	if request.method == 'POST':
		try:
			type = ExpressType.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find express_type which id is [%s].\n Error Message: %s' %(id,err))
			result['success'] = False
			result['message'] = '删除失败，找不到编号为%s的配送方式记录' % id
		
		type.is_delete = True
		type.save()
		
		result['success'] = True
		result['message'] = '配送方式删除成功'
		return JsonResponse(result)
	else:
		raise Http404	

		
@staff_member_required
@transaction.atomic()	
def express_list_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '快递公司管理'
	
	if request.method == 'GET':
		express_list = Express.objects.filter(is_delete=False)
		express_list, page_range = my_pagination(request=request, queryset=express_list,display_amount=15)
		ctx['express_list'] = express_list
		ctx['page_range'] = page_range
		ctx['item_count'] = Express.objects.all().count()
		ctx['page_size'] = 15
		
		
		return render(request,System_Config.get_template_name('admin') + '/express_list.html',ctx)
	else:
		raise Http404
		
		
@staff_member_required
@transaction.atomic()	
def express_edit(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '快递公司管理'
	
	if request.method == 'GET':
		try:
			id = request.GET.get('id','')
			express = Express.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find express which id is [%s].\n Error Message: %s' %(id,err))
			express = None
		express_type_list = ExpressType.objects.filter(is_delete=False)
		ctx['express_type_list'] = express_type_list
		ctx['express'] = express
		return render(request,System_Config.get_template_name('admin') + '/express_detail.html',ctx)
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '快递公司信息保存失败'
		
		express = None
		
		try:
			id = request.POST.get('id','')
			express = Express.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find express which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			
		if express:
			form = express_form(request.POST,instance=express)
		else:
			form = express_form(request.POST)
			
		if form.is_valid():
			express = form.save()
				
			express_type_id_list = request.POST.getlist('express_type')
			express_type_list = ExpressType.objects.filter(id__in=express_type_id_list)
			express.express_type = express_type_list
			express.save()
			
			result['success'] = True
			result['message'] = '快递公司信息保存成功'
			result['express_id'] = express.id
		
		return JsonResponse(result)		
	else:
		raise Http404		
		
@staff_member_required
@transaction.atomic()	
def express_delete(request,id):
	result = {}
	result['success'] = False
	result['message'] = ''
	
	if request.method == 'POST':
		try:
			express = Express.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find express which id is [%s].\n Error Message: %s' %(id,err))
			result['success'] = False
			result['message'] = '删除失败，找不到编号为%s的快递公司' % id
		
		express.is_delete = True
		express.save()
		
		result['success'] = True
		result['message'] = '快递公司删除成功'
		return JsonResponse(result)
	else:
		raise Http404	
		
		
		
		
		
		
		
		
		
		
		