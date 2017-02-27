#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,MyUser
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
		size = System_Config.objects.get(name='admin_user_list_page_size').val
	except:
		logger.info('"admin_user_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size
		

@staff_member_required
@transaction.atomic()
def admin_edit(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '分类管理'

	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = '管理员管理操作失败'

	if request.method == 'POST':
		from shopcart.forms import register_form
		form = register_form(request.POST)
		if form.is_valid():
			myuser = MyUser.objects.create_superuser(email=form.cleaned_data['email'].lower(),password=form.cleaned_data['password'],first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username=form.cleaned_data['email'].lower(),gender='1')
			myuser.is_superuser = True
			myuser.is_staff = True
			myuser.save()
			result_dict['success'] = True
			result_dict['message'] = '管理员管理操作成功'
		return JsonResponse(result_dict)
	elif request.method == 'GET':
	
		return render(request,System_Config.get_template_name('admin') + '/user_admin_detail.html',ctx)
	else:
		raise Http404
	
	
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		