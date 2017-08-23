#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import ArticleBusiCategory,System_Config
from shopcart.utils import my_pagination,get_serial_number,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart.forms import article_busi_category_form
from django.template.response import TemplateResponse
import logging
logger = logging.getLogger('icetus.shopcart')

def get_all_category():
	return ArticleBusiCategory.objects.all()
	
def get_page_size():
	try:
		size = System_Config.objects.get(name='admin_article_busi_category_page_size').val
	except:
		logger.info('"admin_article_busi_category_page_size" is not setted.Use default value 8.')
		size = 15
	return size
	
@staff_member_required
@transaction.atomic()	
def list(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '文章分类管理'
	
	if request.method == 'GET':
		#category_list = ArticleBusiCategory.objects.all().order_by('-update_time')
		category_list = ArticleBusiCategory.objects.all().order_by('-sort_order')
		
		count = category_list.count()

			
		page_size = get_page_size()
		category_list, page_range,current_page = my_pagination(request=request, queryset=category_list,display_amount=page_size)	
		
		ctx['category_list'] = category_list
		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['current_page'] = current_page
		ctx['count'] = count

		return TemplateResponse(request,System_Config.get_template_name('admin') + '/article_busi_category_list.html',ctx)
	elif request.method=='POST':
		raise Http404
	else:
		raise Http404
		
		
@staff_member_required
@transaction.atomic()	
def delete(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '文章分类管理'
	
	if request.method=='POST':
		result = {}
		result['success'] = False
		result['message'] = '文章分类删除失败'
		category = None
		
		try:
			id_list = request.POST.getlist('is_oper')
			for id in id_list:
				category = ArticleBusiCategory.objects.get(id=id)
				category.delete()
		except Exception as err:
			logger.info('Can not find ArticleBusiCategory which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			result['message'] = '删除编号为[%s]的文章分类时出错' % id
			return JsonResponse(result)
		
		result['success'] = True
		result['message'] = '文章分类删除成功'
		result['category_id'] = category.id
		return JsonResponse(result)	
		
	else:
		raise Http404


@staff_member_required
@transaction.atomic()	
def sort(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '文章分类管理'
	
	if request.method=='POST':
		result = {}
		result['success'] = False
		result['message'] = '文章分类排序失败'
		category = None
		
		try:
			id_list = request.POST.getlist('is_oper')
			for id in id_list:
				category = ArticleBusiCategory.objects.get(id=id)
				category.sort_order = request.POST.get('sort_order_%s' % id)
				category.save()
		except Exception as err:
			logger.info('Can not find ArticleBusiCategory which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			result['message'] = '对编号为[%s]的文章分类重排序时出错' % id
			return JsonResponse(result)
		
		result['success'] = True
		result['message'] = '文章分类排序成功'
		result['category_id'] = category.id
		return JsonResponse(result)	
		
	else:
		raise Http404		
	
	

@staff_member_required
@transaction.atomic()	
def edit(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '文章分类管理'
	
	if request.method == 'GET':
		id = request.GET.get('id','')
		try:
			category = ArticleBusiCategory.objects.get(id=id)
			ctx['category'] = category
		except Exception as err:
			logger.error("Can not find ArticleBusiCategory which id is %s . \n Error message: %s" % (id,err))

		#加载自定义模板供选择
		from .file import file_list
		template_list = file_list(System_Config.get_template_name('client') + '/custmize/','custmize_template_article_category')
		logger.debug('>>>>>>>>>>>>>>>>>>custmize_template_article_category: %s' % template_list)
		ctx['custmize_template'] = template_list

			
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/article_busi_category_detail.html',ctx)
	elif request.method=='POST':
		result = {}
		result['success'] = False
		result['message'] = '文章分类保存失败'
		category = None
		
		try:
			id = request.POST.get('id','')
			category = ArticleBusiCategory.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find ArticleBusiCategory which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			
		if category:
			form = article_busi_category_form(request.POST,instance=category)
		else:
			form = article_busi_category_form(request.POST)
			
		if form.is_valid():
			category = form.save()			
			result['success'] = True
			result['message'] = '文章分类保存成功'
			result['category_id'] = category.id
		return JsonResponse(result)	
		
	else:
		raise Http404	
