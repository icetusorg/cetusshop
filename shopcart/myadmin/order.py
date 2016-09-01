#coding=utf-8
from django.shortcuts import render,redirect,render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config,Express,Order,OrderRemark
from shopcart.utils import System_Para,my_pagination,get_serial_number,get_system_parameters
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

def get_page_size():
	try:
		size = System_Config.objects.get(name='admin_order_list_page_size').val
	except:
		logger.info('"admin_order_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size

@staff_member_required
def detail(request,id=None):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = 'Order Detail'
	try:
		order = Order.objects.get(id=id)
	except Exception as err:
		logger.error("Can not find order which id is %s" % id)
		raise Http404
	
	#快递列表
	express_list = Express.objects.all()
	ctx['express_list'] = express_list
	
	ctx['order'] = order
	return render(request,System_Config.get_template_name('admin') + '/order_detail.html',ctx)
	
	
@staff_member_required
def view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = 'Order List'
	
	return render(request,System_Config.get_template_name('admin') + '/order_list.html',ctx)
	

@staff_member_required
@permission_required('shopcart.can_list_order', login_url=NO_PERMISSION_PAGE)
def list_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '订单管理'
	
	if request.method == 'GET':
		order_number = request.GET.get('order_number','')
		ctx['order_number'] = order_number
		user_email = request.GET.get('user_email','')
		ctx['user_email'] = user_email
		
		all = Order.objects.all()
		
		if order_number != '':
			all = all.filter(order_number=order_number)
		
		if user_email != '':
			all = all.filter(user__email=user_email)
		
		
		page_size = get_page_size()
		order_list, page_range = my_pagination(request=request, queryset=all,display_amount=page_size)
		
		ctx['order_list'] = order_list
		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['order_count'] = all.count()
		return render(request,System_Config.get_template_name('admin') + '/order_list_content.html',ctx)
	else:
		raise Http404

@staff_member_required
@transaction.atomic()
def ship(request):	
	result_dict = {}
	message_dict = {}
	if request.method == 'POST':
		order_id = request.POST.get('order_id','')
		express_id = request.POST.get('express_id','')
		shpping_no = request.POST.get('shpping_no','')
		try:
			order = Order.objects.get(id=order_id)
			express = Express.objects.get(id=express_id)
		except:
			logger.error('Can not find order which id is %s' % (order_id))
			raise Http404
		
		order.shpping_no = shipping_no
		order.shipper_name = express.name
		order.status = Order.ORDER_STATUS_SHIPPING
		order.save()
				
		result_dict['success'] = True
		message_dict['status'] = _('已发货')
		result_dict['message'] = message_dict
		return JsonResponse(result_dict)
		
	else:
		raise Http404		
		

def remark_add(request):
	result_dict = {}
	if request.method == 'POST':
		try:
			order_id = request.POST.get('order_id','')
			order = Order.objects.get(id=order_id)
			content = request.POST.get('content','')
			user = request.user
			order_remark = OrderRemark.objects.create(order=order,content=content,user=user)
			result_dict['success'] = True
			result_dict['message'] = '订单备注保存成功'
		except Exception as err:
			logger.error('Save OrderRemark which id is [%s] faild. \n Error Message:%s' %(order_id,err))
			result_dict['success'] = False
			result_dict['message'] = '订单备注保存失败'
		return JsonResponse(result_dict)
		
		
@staff_member_required
def oper(request):	
	if request.method == 'POST':
		oper_ids = request.POST.get('oper-ids','')
		if oper_ids == '':
			raise Http404
		else:
			oper_id_list = oper_ids.split(',')
			for id in oper_id_list:
				try:
					order = Order.objects.get(id=id)
					order.delete()
				except:
					logger.info('Can not find order which id is %s to delete.' % (id))
		return redirect('/admin/order-list/')
	else:
		raise Http404
