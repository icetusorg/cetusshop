#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Product,System_Config,Category
from shopcart.forms import product_add_form,product_basic_info_form,product_detail_info_form
from shopcart.utils import System_Para,handle_uploaded_file,my_pagination
from django.http import Http404,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction

from shopcart.templatetags import shopcart_extras
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

@staff_member_required
def product_opration(request,opration,id):
	ctx = {}
	ctx['system_para'] = System_Para.get_default_system_parameters()
	if request.method == 'GET':
		if opration == 'add':
			if id != '0':
				ctx['image_upload_url'] = '/admin/file-upload/product/%s/' % id
				ctx['edit_url'] = '/admin/shopcart/product/%s/change/' % id
			return render(request,'admin/product/add.html',ctx)
		else:
			raise Http404
	elif request.method == 'POST':
		if opration == 'add':
			form = product_add_form(request.POST)
			if form.is_valid():
				product = form.save()
				logger.debug('product id: %s' % product.id)
				return redirect('/admin/product/add/%s' % product.id)
			else:
				logger.error('form is not valid')
	else:
		raise Http404
		

@staff_member_required
def product_basic_edit(request):
	ctx = {}
	ctx['system_para'] = System_Para.get_default_system_parameters()
	
	result = {}
	result['success'] = False
	result['message'] = ''
	result['data'] = {}
	
	#加载自定义模板供选择
	from .file import file_list
	template_list = file_list(System_Config.get_template_name('client') + '/custmize/','custmize_template_product')
	logger.debug('custome_templates: %s' % template_list)
	ctx['custmize_template'] = template_list
	
	#加载分类树信息
	from shopcart.category import get_all_top_categorys
	top_cat_list = get_all_top_categorys()
	ctx['top_cat_list'] = top_cat_list
	
	#加载属性组
	from shopcart.models import Attribute_Group
	attribute_group_list = Attribute_Group.objects.all();
	ctx['attribute_group_list'] = attribute_group_list
	
	if request.method == 'GET':
		id = request.GET.get('id','')
		
		if id != '':
			try:
				product = Product.objects.get(id=id)
				ctx['product'] = product
				
				pcl=[]
				for cat in product.categorys.all():
					pcl.append(cat.id)
				
				ctx['product_category_id_list'] = pcl
				
			except Exception as err:
				logger.error('Can not find product which id is %s. The error message is %s' % (id,err))
		return render(request,System_Config.get_template_name('admin') + '/product_detail.html',ctx)
	elif request.method == 'POST':
		try:
			product = Product.objects.get(id=request.POST['id'])
			form = product_basic_info_form(request.POST,instance=product)
		except:
			form = product_basic_info_form(request.POST)
			logger.info('New product to store.')
		
		if form.is_valid():
			product = form.save()
			result['success'] = True
			result['message'] = '商品保存成功'
			data = {}
			data['product_id'] = product.id
			result['data'] = data
			#return redirect('/admin/product-edit/?id=%s' % product.id)
		else:
			#return HttpResponse('商品保存失败，请重试。') 
			result['success'] = False
			result['message'] = '商品保存失败'
			result['data'] = {}
		return JsonResponse(result)
	else:
		raise Http404	

		
@staff_member_required
@transaction.atomic()
def product_detail_info_manage(request):
	result = {}
	result['success'] = False
	result['message'] = ''
	if request.method == 'POST':
		try:
			product = Product.objects.get(id=request.POST['id'])
			form = product_detail_info_form(request.POST,instance=product)
		except Exception as err:
			logger.error('Error: %s' % err)
			raise Http404
		
		if form.is_valid():
			product = form.save()
			#处理商品归属的分类
			category_id_list = request.POST.get('product_category_list','')
			if category_id_list:
				category_list = Category.objects.filter(id__in=category_id_list.split(","))
				logger.debug('category_list:%s' % category_list)
				product.categorys = category_list
				product.save()
			else:
				product.categorys = []
				product.save()
			
			result['success'] = True
			result['message'] = '商品详细信息保存成功'
		else:
			result['message'] = '商品详细信息保存失败'
		return JsonResponse(result) 
	elif request.method == 'GET':
		raise Http404
	else:
		raise Http404		
		
		

@staff_member_required
def oper(request):	
	if request.method == 'POST':
		method = request.POST['oper-method']
		oper_ids = request.POST.get('oper-ids','')
		if oper_ids == '':
			raise Http404
		else:
			oper_id_list = oper_ids.split(',')
		
			if method == 'delete':
				for id in oper_id_list:
					try:
						product = Product.objects.get(id=id)
						product.delete()
					except:
						logger.info('Can not find product which id is %s to delete.' % (id))
						
			elif method == 'onpublish' or method == 'offpublish':
				for id in oper_id_list:
					try:
						product = Product.objects.get(id=id)
						if method == 'onpublish':
							product.is_publish = True
						else:
							product.is_publish = False
						product.save()
					except:
						logger.info('Can not find product which id is %s to delete.' % (id))
						
		return redirect('/admin/product/')
	else:
		raise Http404		
		

@staff_member_required
def product_list(request):
	ctx = {}
	ctx['system_para'] = System_Para.get_default_system_parameters()
	if request.method == 'GET':
		
		name_condition = request.GET.get('name','')
		item_number_condition = request.GET.get('item_number','')
		from django.db.models import Q
		product_list = Product.objects.filter(Q(name__icontains=name_condition)).filter(Q(item_number__icontains=item_number_condition))
		#icontains是大小写不敏感的，contains是大小写敏感的
			
		if 'page_size' in request.GET:
			page_size = request.GET['page_size']
		else:
			try:
				page_size = int(System_Config.objects.get(name='admin_product_list_page_size').val)
			except:
				page_size = 12
		
		product_list, page_range = my_pagination(request=request, queryset=product_list,display_amount=page_size)
		ctx['product_list'] = product_list
		ctx['page_range'] = page_range
		ctx['item_count'] = Product.objects.all().count()
		ctx['page_size'] = page_size
		ctx['query_item_number'] = item_number_condition
		ctx['query_name'] = name_condition
		return render(request,System_Config.get_template_name('admin') + '/product_list_content.html',ctx)
	else:
			raise Http404
	
		
		
@staff_member_required
def product_make_static(request):
	ctx = {}
	ctx['product_list'] = Product.objects.all()
	return render(request,'admin/product/make_static.html',ctx)
	
def product_edit(request,id):
	logger.info('Enter into the product_edit function.')
	if request.method=='POST':
		try:
			product = Product.objects.get(id=id)
			product.description = request.POST['editor']
			product.save()
			return HttpResponse('成功')
		except Exception as err:
			logger.error('The Product which id is %s can not found.' % [id])
			raise Http404
	else:
		raise Http404