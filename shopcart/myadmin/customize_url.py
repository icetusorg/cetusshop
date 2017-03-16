#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,CustomizeURL,Article
from shopcart.utils import my_pagination,get_system_parameters
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,Http404
import logging,json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from django.db import transaction
from shopcart.myadmin.utils import NO_PERMISSION_PAGE

import logging
logger = logging.getLogger('icetus.shopcart')

def get_page_size():
	try:
		size = System_Config.objects.get(name='admin_customize_url_list_page_size').val
	except:
		logger.info('"admin_customize_url_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size


@staff_member_required
def detail(request,id=None):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '自定义URL管理'
	try:
		customize_url = CustomizeURL.objects.get(id=id)
	except Exception as err:
		logger.error("Can not find customize_url which id is %s" % id)
		raise Http404
	
	if request.method == 'GET':
		ctx['customize_url'] = customize_url
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/cust_url_detail.html',ctx)
	else:
		result = {}
		result['success'] = False
		result['message'] = '自定义URL保存失败'
		
		from shopcart.forms import customize_url_detail_form
		form = customize_url_detail_form(request.POST,instance=customize_url)
		
		if form.is_valid():
			customize_url = form.save()
			result['success'] = True
			result['message'] = '自定义URL保存成功'
		
		return JsonResponse(result)
		

@staff_member_required
def list_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '自定义URL管理'
	
	if request.method == 'GET':
		url_list = CustomizeURL.objects.all().order_by('-update_time')
		article_list = Article.objects.exclude(category=Article.ARTICLE_CATEGORY_BLOG).order_by('-update_time')

		#count = url_list.count()
		#page_size = get_page_size()
		#url_list, page_range = my_pagination(request=request, queryset=url_list,display_amount=page_size)	

		#ctx['page_range'] = page_range
		#ctx['page_size'] = page_size
		#ctx['page_count'] = count
		
		ctx['url_list'] = url_list
		ctx['article_list'] = article_list
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/cust_url_list.html',ctx)
	else:
		raise Http404


	
	
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		