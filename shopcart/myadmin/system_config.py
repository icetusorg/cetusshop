#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,Email
from shopcart.utils import System_Para,get_system_parameters
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,Http404
import logging,json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.db import transaction
from shopcart.myadmin.utils import NO_PERMISSION_PAGE


# Get an instance of a logger
import logging
logger = logging.getLogger('icetus.shopcart')

	
@staff_member_required
def view(request,type='site_config'):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '系统配置'
	ctx['current_page'] = type
	
	#邮件设置
	email_list = Email.objects.all()
	ctx['email_list'] = email_list
	
	
	template_name = '/system_%s.html' % type
	return render(request,System_Config.get_template_name('admin') + template_name ,ctx)

@staff_member_required
@transaction.atomic()	
def save_config_items(request,is_create=True,is_continue_if_not_exist=True):
	#遍历POST中的参数，找出system_config_开头的参数
	for key in request.POST.keys():
		if key.startswith('system_config_'):
			value = request.POST[key]
			db_key = key[len('system_config_'):len(key)]
			config = None
			try:
				config = System_Config.objects.get(name=db_key)
			except Exception as err:
				logger.info('The system config item [%s] is not exist.' % db_key)
				
			if not config:	
				if is_create:
					config = System_Config.objects.create(name=db_key)
				else:
					if is_continue_if_not_exist:
						continue
					else:
						raise Exception('SystemConfigDosNotExits')
			config.val = value
			config.save()

			
@staff_member_required
@transaction.atomic()	
def pay_config(request,pay_type):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '支付管理'
	if request.method == 'GET':	
		if pay_type == 'paypal':
			account = ''
			env = 'sandbox'
			
			try:
				account = System_Config.objects.get(name='paypal_account').val
				env = System_Config.objects.get(name='paypal_env').val
			except Exception as err:
				logger.debug('Can not find paypal config.\n Error Message:%s' % err)
		
			ctx['paypal_account'] = account
			ctx['paypal_env'] = env
		
			return render(request,System_Config.get_template_name('admin') + '/payment/paypal.html' ,ctx)
		else:
			raise Http404
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '支付配置信息保存失败'
		
		account_name = request.POST.get('paypal_account','')
		env_name = request.POST.get('paypal_env','')
		
		try:
			account,a_created = System_Config.objects.get_or_create(name='paypal_account')
			env,e_created = System_Config.objects.get_or_create(name='paypal_env')
		except Exception as err:
			logger.error('Can not find or create paypal config.\n Error Message: %s' % err)
			result['success'] = False
			result['message'] = '支付配置信息无法保存，可能存在风险，请检查数据库中是否存在多条paypal配置信息。'
			return JsonResponse(result)
		
		account.val = account_name
		account.save()
		env.val = env_name
		env.save()
		result['success'] = True
		result['message'] = '支付配置信息保存成功'
	
		return JsonResponse(result)
	else:
		raise Http404	
	
			
			
@staff_member_required
@transaction.atomic()
def display_config_manage(request):
	result = {}
	result['success'] = False
	result['message'] = ''
	if request.method == 'POST':		
		try:
			save_config_items(request)
			result['success'] = True
			result['message'] = '显示设置保存成功'
		except Exception as err:
			result['message'] = '显示保存失败'

		return JsonResponse(result) 
	elif request.method == 'GET':
		raise Http404
	else:
		raise Http404	


@staff_member_required
@transaction.atomic()
def email_config_manage(request):
	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = ''
	

		from shopcart.forms import email_form
		id = request.POST.get('id','')

		try:
			email = Email.objects.get(id=id)
			form = email_form(request.POST,instance=email)
			form.save()
		except Exception as err:
			logger.error('Save email config which id is [%s] faild. \n Error message: %s' % (id,err))
			result['message'] = '邮件设置保存失败'
			return JsonResponse(result)

		result['success'] = True
		result['message'] = '邮件设置保存成功'
		return JsonResponse(result) 
	elif request.method == 'GET':
		ctx = {}
		ctx['system_para'] = get_system_parameters()
		ctx['page_name'] = '邮件配置'
	
		id = request.GET.get('id','')
		try:
			email = Email.objects.get(id=id)
			ctx['email'] = email
		except Exception as err:
			logger.error('Can not find email setting which id is [%s]' % id)
			raise Http404
			
		return render(request,System_Config.get_template_name('admin') + '/system_email_detail_config.html' ,ctx)
	else:
		raise Http404	
		
	
@staff_member_required
@transaction.atomic()
def site_config_manage(request):
	result = {}
	result['success'] = False
	result['message'] = ''
	if request.method == 'POST':
		#logger.debug('POST:%s' % request.POST)
		
		try:
			save_config_items(request)
			result['success'] = True
			result['message'] = '网站信息保存成功'
		except Exception as err:
			result['message'] = '网站信息保存失败'

		return JsonResponse(result) 
	elif request.method == 'GET':
		raise Http404
	else:
		raise Http404	