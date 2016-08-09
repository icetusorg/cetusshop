#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Product,System_Config
from shopcart.forms import product_add_form
from shopcart.utils import System_Para,handle_uploaded_file
from django.http import Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
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
def product_list(request):
	ctx = {}
	ctx['system_para'] = System_Para.get_default_system_parameters()
	if request.method == 'GET':
		product_list = Product.objects.all()
		ctx['product_list'] = product_list
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