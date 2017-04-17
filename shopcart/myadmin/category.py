#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Category,System_Config
from shopcart.utils import my_pagination,get_serial_number,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart import category as category_util
from shopcart.forms import category_form,category_simple_form
from django.template.response import TemplateResponse
import logging
logger = logging.getLogger('icetus.shopcart')

	
@staff_member_required
@transaction.atomic()	
def list_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '分类管理'
	
	if request.method == 'GET':
		title = request.GET.get('title','')
		ctx['title'] = title

		
		top_category_list = category_util.get_all_top_categorys()
		
		ctx['category_list'] = top_category_list
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/category_list.html',ctx)
	else:
		raise Http404
	
@staff_member_required
@transaction.atomic()	
def ajax_add_category(request):
	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '分类信息保存失败'
		
		form = category_simple_form(request.POST)
		
		logger.debug('1111')
		if form.is_valid():
			category = form.save()
			parent_id = request.POST.get('parent_id','')
			if parent_id != '':
				try:
					parent = Category.objects.get(id=parent_id)
					category.parent = parent
					category.save()
				except Exception as err:
					logger.info('Can not find category which id is [%s]. Create one. \n Error Message: %s' %(id,err))
					return JsonResponse(result)
				
			result['success'] = True
			result['message'] = '分类信息保存成功'
			result['category_id'] = category.id

		return JsonResponse(result)		
	
	else:
		raise Http404	
	
	
@staff_member_required
@transaction.atomic()	
def oper(request,method):
	if request.method == 'POST':
		result={}
		if method == 'set_order':
			id_list = request.POST.getlist('selected')
			for id in id_list:
				try:
					cat = Category.objects.get(id=id)
				except Exception as err:
					logger.error('Can not find category %s .\n Error Message: %s' % (id,err))
					cat = None
				if cat:
					try:
						sort = request.POST.get('sort_%s' % id)
					except:
						sort = None
					if sort:
						cat.sort_order = sort
						cat.save()
			result['success'] = True
			result['message'] = '分类信息保存成功'
		
			return JsonResponse(result)
		else:
			raise Http404
	else:
		raise Http404
	
	
@staff_member_required
@transaction.atomic()	
def delete(request,id):
	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '分类信息删除失败'
			
		try:
			category = Category.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find category which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			return JsonResponse(result)
		
		#判断category有没有子分类
		sub_category_count = category.childrens.all().count()
		logger.info('Category [%s] has [%s] sub_categorys.' % (category.name,sub_category_count))
		if sub_category_count > 0:
			result['success'] = False
			result['message'] = '该分类下存在子分类，请先删除子分类。'
			return JsonResponse(result)
		
		#判断category有没有被关联到商品
		product_count = category.products.all().count()
		logger.info('Category [%s] has [%s] products.' % (category.name,product_count))
		
		if product_count > 0:
			result['success'] = False
			result['message'] = '该分类下存在 %s 件商品，请先将商品移动到其它分类。' % product_count
			return JsonResponse(result)
		
		category.delete()
		result['success'] = True
		result['message'] = '分类信息删除成功'

		return JsonResponse(result)		
	
	else:
		raise Http404
	
	
	
@staff_member_required
@transaction.atomic()	
def edit(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '分类管理'
		
	
	if request.method == 'GET':
		#加载自定义模板供选择
		from .file import file_list
		template_list = file_list(System_Config.get_template_name('client') + '/custmize/','custmize_template_category')
		logger.debug('custome_templates: %s' % template_list)
		ctx['custmize_template'] = template_list
		
		
		#加载商品详情页模板供选择
		template_product_list = file_list(System_Config.get_template_name('client') + '/custmize/','custmize_template_product')
		logger.debug('custome_templates: %s' % template_product_list)
		ctx['custmize_product_template'] = template_product_list
	
	
		try:
			id = request.GET.get('id','')
			category = Category.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find Category which id is [%s].\n Error Message: %s' % (id,err))
			category = None
		
		ctx['category'] = category
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/category_detail.html',ctx)
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '分类信息保存失败'
		
		category = None
		
		try:
			id = request.POST.get('id','')
			category = Category.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find category which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			
		if category:
			form = category_form(request.POST,instance=category)
		else:
			form = category_form(request.POST)
			#form = category_simple_form(request.POST)
		
		logger.debug("aaaa")
		logger.debug('name:' + request.POST.get('name'))
		
		
		if form.is_valid():
			category = form.save()			
			result['success'] = True
			result['message'] = '分类信息保存成功'
			result['category_id'] = category.id
		else:
			logger.debug('form not valid')

		return JsonResponse(result)		
	
	else:
		raise Http404	