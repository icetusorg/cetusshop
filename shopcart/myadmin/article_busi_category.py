#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import ArticleBusiCategory,System_Config
from shopcart.utils import System_Para,my_pagination,get_serial_number,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart.forms import article_busi_category_form
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
def edit(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '文章分类管理'
	
	if request.method == 'GET':
		id = request.GET.get('id','')
		try:
			category = ArticleBusiCategory.objects.get(id=id)
			ctx['category'] = category
			return render(request,System_Config.get_template_name('admin') + '/article_busi_category_detail.html',ctx)
		except Exception as err:
			logger.error("Can not find ArticleBusiCategory which id is %s . \n Error message: %s" % (id,err))
			
		return render(request,System_Config.get_template_name('admin') + '/article_busi_category_detail.html',ctx)
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
