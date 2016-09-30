#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Category,System_Config
from shopcart.utils import System_Para,my_pagination,get_serial_number,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart import category as category_util
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
		return render(request,System_Config.get_template_name('admin') + '/category_list.html',ctx)
	else:
		raise Http404
	