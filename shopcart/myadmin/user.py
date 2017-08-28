#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,MyUser,Reset_Password
from shopcart.utils import my_pagination,get_system_parameters
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,Http404
import logging,json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.db import transaction
from shopcart.myadmin.utils import NO_PERMISSION_PAGE
from shopcart import signals




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
def user_list(request):
	ctx = {}
	ctx['page_name'] = '用户管理'

	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = '用户信息保存失败'

	if request.method == 'GET':
		#user_list = MyUser.objects.filter(is_staff=False).filter(is_superuser=False).order_by('-update_time')
		#user_list = MyUser.objects.order_by('-update_time')
		user_list = MyUser.objects.order_by('-create_time')
		
		item_value = request.GET.get('item_value','')
		
		if item_value:
			from django.db.models import Q
			user_list = user_list.filter(Q(email__icontains=item_value))
			
		count = len(user_list)
	
		page_size = get_page_size()
		user_list, page_range,current_page = my_pagination(request=request, queryset=user_list,display_amount=page_size)	
		
		ctx['user_list'] = user_list
		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['current_page'] = current_page
		ctx['item_count'] = count
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/user_list.html',ctx)
	else:
		raise Http404		
		
@staff_member_required
@transaction.atomic()
def user_delete(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '用户管理'

	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = '用户删除失败'

	if request.method == 'POST':	
		user_id_list = request.POST.getlist('is_oper')
		try:
			for id in user_id_list:
				myuser = MyUser.objects.get(id=id)
				myuser.delete()
			result_dict['success'] = True
			result_dict['message'] = '用户删除成功'
		except Exception as err:
			logger.info('Can not find user which id=[%s]. \n Error Message : %s' % (id,err))
			

		return JsonResponse(result_dict)
	else:
		raise Http404
		
@staff_member_required
@transaction.atomic()
def user_active(request,active):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '用户管理'

	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = '用户状态保存失败'

	if request.method == 'POST':	
		user_id_list = request.POST.getlist('is_oper')
		status = False
		
		if active=='on':
			status = True
			
		try:
			for id in user_id_list:
				myuser = MyUser.objects.get(id=id)
				myuser.is_active = status
				myuser.save()
			result_dict['success'] = True
			result_dict['message'] = '用户状态保存成功'
		except Exception as err:
			logger.info('Can not find user which id=[%s]. \n Error Message : %s' % (id,err))
		return JsonResponse(result_dict)
	else:
		raise Http404

		
@staff_member_required
@transaction.atomic()
def user_reset_password(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '用户管理'

	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = '用户密码重置失败'

	if request.method == 'POST':	
		user_id_list = request.POST.getlist('is_oper')		
		import uuid,datetime
		try:
			for id in user_id_list:
				myuser = MyUser.objects.get(id=id)
				s_uuid = str(uuid.uuid4())
				reset_password = Reset_Password.objects.create(email=myuser.email,validate_code=s_uuid,apply_time=datetime.datetime.now(),expirt_time=(datetime.datetime.now() + datetime.timedelta(hours=24)),is_active=True)
			
				#触发用户申请重置密码的事件	
				signals.user_password_modify_applied.send(sender='MyUser',reset_password=reset_password)
			
			result_dict['success'] = True
			result_dict['message'] = '用户密码重置请求已发出，请用户在24小时内点击邮件内链接重新设置密码。'
		except Exception as err:
			logger.info('Can not find user which id=[%s]. \n Error Message : %s' % (id,err))
		return JsonResponse(result_dict)
	else:
		raise Http404		
		
		
		

@staff_member_required
@transaction.atomic()
def admin_edit(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '用户管理'

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
	
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/user_admin_detail.html',ctx)
	else:
		raise Http404
	
	
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		