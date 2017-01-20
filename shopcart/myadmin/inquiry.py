#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,Inquiry,Product
from shopcart.utils import System_Para,my_pagination,get_system_parameters
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,Http404
import logging,json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.db import transaction
from shopcart.myadmin.utils import NO_PERMISSION_PAGE

import logging
logger = logging.getLogger('icetus.shopcart')

def get_page_size():
	try:
		size = System_Config.objects.get(name='admin_inquiry_list_page_size').val
	except:
		logger.info('"admin_inquiry_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size


@staff_member_required
def detail(request,id=None):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = 'Inquiry Detail'
	try:
		inquiry = Inquiry.objects.get(id=id)
	except Exception as err:
		logger.error("Can not find inquiry which id is %s" % id)
		raise Http404
	
	get_product_detail_for_inquiry(inquiry)		
	ctx['inquiry'] = inquiry
	
	return render(request,System_Config.get_template_name('admin') + '/inquiry_detail.html',ctx)


def get_product_detail_for_inquiry(inquiry):
	p = None
	if inquiry.product > 0:
		try:
			p = Product.objects.get(id = inquiry.product)
		except:
			logger.info('Inquiry which id=[%s] can not find product which id=[%s]' % (inquiry.id,inquiry.product))
	inquiry.product_detail = p
	

@staff_member_required
def list_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '订单管理'
	
	if request.method == 'GET':
		inquiry_list = Inquiry.objects.all()
		
		qry_field = request.GET.get('qry_field','')
		qry_value = request.GET.get('qry_value','')
		if qry_field:
			from django.db.models import Q
			if qry_field == 'email':
				inquiry_list = inquiry_list.filter(Q(email__icontains=qry_value))
			elif qry_field == 'title':
				inquiry_list = inquiry_list.filter(Q(title__icontains=qry_value))
			elif qry_field == 'message':
				inquiry_list = inquiry_list.filter(Q(message__icontains=qry_value))
			else:
				pass
		
		count = inquiry_list.count()
		
		for inquiry in inquiry_list:
			get_product_detail_for_inquiry(inquiry)
			
		page_size = get_page_size()
		inquiry_list, page_range = my_pagination(request=request, queryset=inquiry_list,display_amount=page_size)	
		
		ctx['inquiry_list'] = inquiry_list
		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['inquiry_count'] = count
		return render(request,System_Config.get_template_name('admin') + '/inquiry_list.html',ctx)
	else:
		raise Http404

		

@staff_member_required
@transaction.atomic()
def delete(request):
	result_dict = {}
	result_dict['success'] = True
	result_dict['message'] = '留言删除失败'

	if request.method == 'POST':
		id_list = request.POST.getlist("inquiry_id")
				
		err_count = 0
		for id in id_list:
			try:
				inquiry = Inquiry.objects.get(id=id)
				inquiry.delete()
			except:
				err_count = err_count + 1
		
		if err_count > 0:
			result_dict['message'] = '部分留言删除失败，或者已经备别的操作员删除，请查询确认。'
		else:
			result_dict['message'] = '留言删除成功'
		
		return JsonResponse(result_dict)
	else:
		raise Http404
	
	
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		