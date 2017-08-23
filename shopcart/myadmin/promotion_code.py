#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,Promotion
from shopcart.utils import my_pagination
from shopcart.forms import promotion_detail_form
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
		size = System_Config.objects.get(name='admin_promotion_list_page_size').val
	except:
		logger.info('"admin_promotion_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size



@staff_member_required
@transaction.atomic()
def list(request):
	ctx = {}
	ctx['page_name'] = '优惠码管理'
	
	if request.method == 'GET':
		promotion_list = Promotion.objects.all().order_by('-create_time')


		count = promotion_list.count()
		page_size = get_page_size()
		promotion_list, page_range,current_page = my_pagination(request=request, queryset=promotion_list,display_amount=page_size)	

		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['current_page'] = current_page
		ctx['item_count'] = count
		
		ctx['promotion_list'] = promotion_list
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/promotion_list.html',ctx)
	else:
		raise Http404
		
@staff_member_required
@transaction.atomic()		
def oper(request,method):
	result = {}
	if request.method == "POST":
		if method == 'delete':
			id_list = request.POST.getlist('is_oper')
			promotion_list = Promotion.objects.filter(id__in = id_list)
			for p in promotion_list:
				p.delete()
			result['success'] = True
			result['message'] = '优惠码删除成功'
			return JsonResponse(result)
		else:
			raise Http404
	else:
		raise Http404
				
		
		
@staff_member_required
@transaction.atomic()
def detail(request):
	ctx = {}
	ctx['page_name'] = '优惠码管理'
	
	if request.method == 'GET':
		id = request.GET.get('id','')
		try:
			promotion = Promotion.objects.get(id=id)
		except Exception as err:
			promotion = None
		ctx['promotion'] = promotion
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/promotion_detail.html',ctx)
	elif request.method == 'POST':
		id = request.POST.get('id','')
		try:
			promotion = Promotion.objects.get(id=id)
			form = promotion_detail_form(request.POST,instance=promotion)
		except Exception as err:
			promotion = None
			form = promotion_detail_form(request.POST)
			logger.info('New promotion to store.')
			
		result = {}
		
		if form.is_valid():
			promotion = form.save()
			result['success'] = True
			result['message'] = '优惠码保存成功'
			data = {}
			data['promotion_id'] = promotion.id
			result['data'] = data	
		else:
			result['success'] = False
			result['message'] = '优惠码保存失败，参数没有填写完整。'
		return JsonResponse(result)	
		
	else:
		raise Http404


	
	
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		