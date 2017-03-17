#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Product,System_Config,Category,Attribute,Attribute_Group,Product_Attribute,Product_Images,ProductParaGroup,ProductPara,ProductPrice,ProductParaDetail,Album
from shopcart.forms import product_add_form,product_basic_info_form,product_detail_info_form,product_para_group_form,product_sku_group_form
from shopcart.utils import handle_uploaded_file,my_pagination
from django.http import Http404,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.db import transaction

from shopcart.templatetags import shopcart_extras
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


@staff_member_required
@transaction.atomic()
def product_sku_group_edit(request):
	ctx = {}
	
	ctx['page_name'] = '商品SKU组管理'
	
	if request.method == 'GET':
		try:
			id = request.GET.get('id','')
			sku_group = Attribute_Group.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find Attribute_Group which id is [%s].\n Error Message: %s' % (id,err))
			sku_group = None
		
		ctx['sku_group'] = sku_group
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/product_sku_group_detail.html',ctx)
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '商品SKU组保存失败'
		
		sku_group = None
		
		try:
			id = request.POST.get('sku_group_id','')
			sku_group = Attribute_Group.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find Attribute_Group which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			
		if sku_group:
			form = product_sku_group_form(request.POST,instance=sku_group)
		else:
			form = product_sku_group_form(request.POST)
			
		if form.is_valid():
			sku_group = form.save()
			
			result['success'] = True
			result['message'] = '商品SKU组保存成功'
			result['sku_group_id'] = sku_group.id
		return JsonResponse(result)		
	else:
		raise Http404		


@staff_member_required
@transaction.atomic()
def product_sku_group_list(request):
	ctx = {}
	
	if request.method == 'GET':
		group_list = Attribute_Group.objects.all()
		
		page_size = 12
		group_list, page_range = my_pagination(request=request, queryset=group_list,display_amount=page_size)
		ctx['group_list'] = group_list
		ctx['page_range'] = page_range
		ctx['item_count'] = ProductParaGroup.objects.all().count()
		ctx['page_size'] = page_size
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/product_sku_group_list.html',ctx)
	else:
			raise Http404		
		

@staff_member_required
@transaction.atomic()
def product_para_list(request):
	ctx = {}
	
	if request.method == 'GET':
		product_para_list = ProductParaGroup.objects.all()
		
		page_size = 12
		product_para_list, page_range = my_pagination(request=request, queryset=product_para_list,display_amount=page_size)
		ctx['product_para_list'] = product_para_list
		ctx['page_range'] = page_range
		ctx['item_count'] = ProductParaGroup.objects.all().count()
		ctx['page_size'] = page_size
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/product_para_list_content.html',ctx)
	else:
			raise Http404

@staff_member_required
@transaction.atomic()
def product_para_group_edit(request):
	ctx = {}
	
	ctx['page_name'] = '商品参数组管理'
	
	if request.method == 'GET':
		try:
			id = request.GET.get('id','')
			para_group = ProductParaGroup.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find ProductParaGroup which id is [%s].\n Error Message: %s' % (id,err))
			para_group = None
		
		ctx['para_group'] = para_group
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/product_para_detail.html',ctx)
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '商品参数组保存失败'
		
		para_group = None
		
		try:
			id = request.POST.get('para_group_id','')
			para_group = ProductParaGroup.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find para_group which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			
		if para_group:
			form = product_para_group_form(request.POST,instance=para_group)
		else:
			form = product_para_group_form(request.POST)
			
		if form.is_valid():
			para_group = form.save()
			
			result['success'] = True
			result['message'] = '商品参数组保存成功'
			result['para_group_id'] = para_group.id
		return JsonResponse(result)		
	else:
		raise Http404
	
@staff_member_required
@transaction.atomic()
def product_sku_group_delete(request):
	ctx = {}
	
	ctx['page_name'] = '商品SKU组管理'
	
	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '商品SKU组删除失败'
		
		
		try:
			id_list = request.POST.getlist('is_oper')
			for id in id_list:
				group = Attribute_Group.objects.get(id=id)
				group.delete()
		except Exception as err:
			logger.info('Can not find Attribute_Group which id is [%s]. \n Error Message: %s' %(id,err))
			return JsonResponse(result)
			

		result['success'] = True
		result['message'] = '商品SKU组删除成功'
		return JsonResponse(result)		
	else:
		raise Http404	


	
@staff_member_required
@transaction.atomic()
def product_para_group_delete(request):
	ctx = {}
	
	ctx['page_name'] = '商品参数组管理'
	
	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '商品参数组删除失败'
		
		
		try:
			id_list = request.POST.getlist('is_oper')
			for id in id_list:
				para_group = ProductParaGroup.objects.get(id=id)
				para_group.delete()
		except Exception as err:
			logger.info('Can not find para_group which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			return JsonResponse(result)
			

		result['success'] = True
		result['message'] = '商品参数组删除成功'
		return JsonResponse(result)		
	else:
		raise Http404			
		
		
@staff_member_required
@transaction.atomic()
def product_sku_item_edit(request):
	ctx = {}
	
	ctx['page_name'] = 'SKU项目管理'
	
	if request.method == 'GET':
		raise Http404
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = 'SKU项目保存失败'
		
		attribute = None
		name = request.POST.get('name','')
		code = request.POST.get('code','')
		position = request.POST.get('position','0')
		try:
			attribute = Attribute.objects.get(id=request.POST.get('attribute_id',''))
		except Exception as err:
			logger.info('Can not find attribute which id is [%s]. Create One. \n Error Message: %s' %(attribute,err))
		
		if attribute:
			attribute.name = name
			attribute.code = code
			attribute.position = position
			attribute.save()
		else:
			group_id = request.POST.get('group_id','')
			try:
				group = Attribute_Group.objects.get(id=group_id)
			except Exception as err:
				logger.info('Can not find Attribute_Group which id is [%s].  \n Error Message: %s' %(group_id,err))
				result['message'] = '无法找到编号为%s的SKU组，可能已经被删除。' % group_id
				return JsonResponse(result)
				
			attribute = Attribute.objects.create(group=group,name=name,code=code,position=position)

		
		result['success'] = True
		result['message'] = 'SKU项目保存成功'
		result['new_id'] = attribute.id
		result['attribute_id'] = attribute.id
		return JsonResponse(result)		
	else:
		raise Http404		
		

		
@staff_member_required
@transaction.atomic()
def product_sku_item_set_image(request):
	ctx = {}
	
	ctx['page_name'] = 'SKU项目图片管理'

	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = 'SKU项目图片保存失败'
		
		method = request.POST.get('method','')

		if method == 'set_sku':
			picture_id = request.POST.get('picture_id','')
			sku_id = request.POST.get('sku_id','')
			try:
				sku = Attribute.objects.get(id=sku_id)
			except Exception as err:
				logger.info('Can not find  sku [%s] . \n Error Message: %s' %(sku_id,err))
				result['message'] = 'SKU项目图片信息保存失败，找不到对应的SKU'
				return JsonResponse(result)

			try:
				picture = Album.objects.get(id=picture_id)
			except Exception as err:
				logger.info('Can not find  picture [%s] in Album. \n Error Message: %s' %(picture_id,err))
				picture = None
					
			if picture:
				sku.thumb = picture.thumb
				sku.save()
				result['thumb'] = picture.thumb
				result['image'] = picture.image
				result['success'] = True
				result['message'] = 'SKU项目图片信息保存成功'
			else:
				result['message'] = 'SKU项目图片信息保存失败，可能图片已经被删除了。'		
			
			return JsonResponse(result)
		elif method == 'delete':
			picture_id = request.POST.get('picture_id','')
			try:
				picture = Album.objects.get(id=picture_id)
				picture.delete()
				result['success'] = True
				result['message'] = 'SKU项目图片信息删除成功'
			except Exception as err:
				logger.info('Can not find  picture [%s] in Album. \n Error Message: %s' %(picture_id,err))
				result['success'] = True
				result['message'] = 'SKU项目图片信息删除失败'
			
			return JsonResponse(result)
			
	else:
		raise Http404		
		
		

@staff_member_required
@transaction.atomic()
def product_para_edit(request):
	ctx = {}
	
	ctx['page_name'] = '商品参数管理'
	
	if request.method == 'GET':
		raise Http404
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '商品参数保存失败'
		
		para_group = None
		try:
			para_group = ProductParaGroup.objects.get(id=request.POST.get('para_group_id',''))
		except Exception as err:
			logger.info('Can not find para_group which id is [%s]. \n Error Message: %s' %(id,err))
			result['message'] = '无法找到编号为%s的参数组，可能已经被删除。' % request.POST.get('para_group_id','')
			return JsonResponse(result)
		
		
		name = request.POST.get('name','')
		
		try:
			id = request.POST.get('id','')
			para = ProductPara.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find para which id is [%s]. Create one. \n Error Message: %s' %(id,err))
			para = ProductPara.objects.create(group=para_group,name=name)
		
		para.name = name
		para.save()
		
		result['success'] = True
		result['message'] = '商品参数信息保存成功'
		result['new_id'] = para.id
		result['para_group_id'] = para_group.id
		return JsonResponse(result)		
	else:
		raise Http404
		
		
@staff_member_required
@transaction.atomic()	
def product_para_detail_create(request):
	result = {}
	result['success'] = False
	result['message'] = ''
	
	if request.method == 'POST':
		product_id = request.POST.get('product_id')
		group_id = request.POST.get('product_para_group')
	
		try:
			product = Product.objects.get(id=product_id)
			group = ProductParaGroup.objects.get(id=group_id)
		except Exception as err:
			logger.error("Can not find product [%s] or group [%s] \n Error message:%s" % (product_id,group_id,err))
			result['message'] = '生成参数组失败，请重试。'
			return JsonResponse(result)
		
		if product.parameters.all():
			result['message'] = '该商品已经存在参数值，如要重新设置，请先执行“清除”操作！';
			return JsonResponse(result)
		
		for para in group.paras.all():
			ProductParaDetail.objects.create(product_para=para,product=product,value='')
			
		result['success'] = True
		result['message'] = '参数组生成成功，请填入相关数据。'
		return JsonResponse(result)

@staff_member_required
@transaction.atomic()	
def product_para_detail_edit(request):
	result = {}
	result['success'] = False
	result['message'] = ''
	
	if request.method == 'POST':
		#遍历POST中的参数，找出product_para_id_开头的参数
		for key in request.POST.keys():
			if key.startswith('product_para_id_'):
				value = request.POST[key]
				db_key = key[len('product_para_id_'):len(key)]
				
				try:
					prd = ProductParaDetail.objects.get(id=db_key)
					prd.value = value
					prd.save()
				except Exception as err:
					logger.error('Can not find parameter [%s]. \n Error Message:%s' %(db_key,err))
					result['message'] = '参数保存失败'
					return JsonResponse(result)
			
		result['success'] = True
		result['message'] = '参数组保存成功'
		return JsonResponse(result)		
		
		
@staff_member_required
@transaction.atomic()
def product_para_delete(request):
	ctx = {}
	
	ctx['page_name'] = '商品参数管理'
	
	if request.method == 'GET':
		raise Http404
	elif request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '商品参数删除失败'
		
		try:
			id = request.POST.get('id','')
			para = ProductPara.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find para which id is [%s]. \n Error Message: %s' %(id,err))
			return JsonResponse(result)
		
		para.delete()
		result['success'] = True
		result['message'] = '商品参数删除成功'
		return JsonResponse(result)		
	else:
		raise Http404
			

@staff_member_required
@transaction.atomic()
def set_image(request):
	ctx = {}
	
	ctx['page_name'] = '商品图片管理'

	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '商品图片信息保存失败'
		
		method = request.POST.get('method','')
		if method == 'set_main':
			try:
				product_id = request.POST.get('item_id','')
				picture_id = request.POST.get('picture_id','')
				product = Product.objects.get(id=product_id)
				picture = Product_Images.objects.get(id=picture_id)
			except Exception as err:
				logger.info('Can not find product [%s] or picture [%s]. \n Error Message: %s' %(product_id,picture_id,err))
				picture = None
			
			product.image = picture.image
			product.thumb = picture.thumb
			product.save()	
			
			result['success'] = True
			result['message'] = '商品图片信息保存成功'
			return JsonResponse(result)
		elif method == 'delete':
			picture_id = request.POST.get('picture_id','')
			picture = None
			
			try:
				picture = Product_Images.objects.get(id=picture_id)
			except Exception as err:
				logger.info('Can not find  picture [%s] in Product_Images. \n Error Message: %s' %(picture_id,err))
				
			if not picture:
				try:
					picture = Album.objects.get(id=picture_id)
				except Exception as err:
					logger.info('Can not find  picture [%s] in Album. \n Error Message: %s' %(picture_id,err))
			
			if picture:
				picture.delete()
				result['success'] = True
				result['message'] = '商品图片信息保存成功'
			else:
				result['message'] = '商品图片信息保存失败，可能图片已经被删除了。'
			
			return JsonResponse(result)
		elif method == 'set_sku':
			picture_id = request.POST.get('picture_id','')
			sku_id = request.POST.get('sku_id','')
			try:
				sku = Product_Attribute.objects.get(id=sku_id)
			except Exception as err:
				logger.info('Can not find  sku [%s] . \n Error Message: %s' %(sku_id,err))
				result['message'] = '商品图片信息保存失败，找不到对应的SKU'
				return JsonResponse(result)

			
			try:
				picture = Product_Images.objects.get(id=picture_id)
			except Exception as err:
				logger.info('Can not find  picture [%s] in Product_Images. \n Error Message: %s' %(picture_id,err))
				
			if not picture:
				try:
					picture = Album.objects.get(id=picture_id)
				except Exception as err:
					logger.info('Can not find  picture [%s] in Album. \n Error Message: %s' %(picture_id,err))
					
			if picture:
				sku.image = picture
				sku.save()
				result['thumb'] = picture.thumb
				result['image'] = picture.image
				result['success'] = True
				result['message'] = '商品图片信息保存成功'
			else:
				result['message'] = '商品图片信息保存失败，可能图片已经被删除了。'		
			
			return JsonResponse(result)
	else:
		raise Http404
			
			

@staff_member_required
@transaction.atomic()
def product_opration(request,opration,id):
	ctx = {}
	
	if request.method == 'GET':
		if opration == 'add':
			if id != '0':
				ctx['image_upload_url'] = '/admin/file-upload/product/%s/' % id
				ctx['edit_url'] = '/admin/shopcart/product/%s/change/' % id
			return TemplateResponse(request,'admin/product/add.html',ctx)
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
@transaction.atomic()
def product_basic_edit(request):
	ctx = {}
	
	
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
	
	#加载商品参数组
	para_group_list = ProductParaGroup.objects.all();
	ctx['product_para_group_list'] = para_group_list
	
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
				
				if product.attributes.all():
					ctx['attribute_group_belong'] = product.attributes.all()[0].get_attribute_groups()
					
					
				#图片处理URL
				ctx['upload_url'] = '/admin/file-upload/product/%s/' % id
				logger.debug('upload_url:%s' % ctx['upload_url'])
				
				#ctx['file_delete_url'] = '/file-delete/product'
					
				
				try:
					ctx['image_list'] = Product_Images.objects.filter(product=product).filter(is_show_in_product_detail=True).order_by('create_time').reverse()
					logger.debug("ctx['image_list']:%s" % ctx['image_list'])
				except Exception as err:
					logger.error("Error:%s" % err)
					ctx['image_list'] = []
				
			except Exception as err:
				logger.error('Can not find product which id is %s. The error message is %s' % (id,err))
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/product_detail.html',ctx)
	elif request.method == 'POST':
		is_new = False
		try:
			product = Product.objects.get(id=request.POST['id'])
			form = product_basic_info_form(request.POST,instance=product)
		except:
			product = None
			form = product_basic_info_form(request.POST)
			is_new = True
			logger.info('New product to store.')
		
		if form.is_valid():
			#判断自定义文件名是否重复
			url = form.cleaned_data['static_file_name']
			if url:
				try:
					p = Product.objects.get(static_file_name=url)
				except Exception as err:
					p = None
					
				if p and p != product:
					#能找到，说明重名了
					result['success'] = False
					result['message'] = '自定义URL与%s商品重复！' % p.name
					return JsonResponse(result)
		
			product = form.save()
			#处理商品分段价格
			if is_new:
				logger.debug('New product.Create price list.')
				for n in [0,1,2]:
					p = ProductPrice.objects.create(product=product,sort_order=n,price=0.0,quantity=0)
			
			
			#处理商品归属的分类
			category_id_list = request.POST.getlist('category_check')
			if category_id_list:
				category_list = Category.objects.filter(id__in=category_id_list)
				logger.debug('category_list:%s' % category_list)
				product.categorys = category_list
				product.save()
			else:
				product.categorys = []
				product.save()
			
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
	result['message'] = '商品详细信息保存失败'
	if request.method == 'POST':
		try:
			product = Product.objects.get(id=request.POST['id'])
			form = product_detail_info_form(request.POST,instance=product)
		except Exception as err:
			logger.error('Error: %s' % err)
			raise Http404
		
		if form.is_valid():
			product = form.save()
			
			#处理商品分段价格
			if not product.prices.all(): #兼容老版本，可能有存量商品没有加过存量价格
				logger.debug('Create price list.')
				for n in [0,1,2]:
					p = ProductPrice.objects.create(product=product,sort_order=n,price=0.0,quantity=0)
					
			#遍历POST中的参数，找出quantity_leve 和 price_level开头的参数
			for n in [0,1,2]:
				quantity = request.POST['quantity_level_%s' % n]
				price = request.POST['price_level_%s' % n]
				try:
					p = ProductPrice.objects.get(product=product,sort_order=n)
					p.quantity = quantity
					p.price = price
					p.save()
				except Exception as err:
					logger.error('Can not find price list in product [%s]. \n Error Message:%s' % (product.id,err))
					return JsonResponse(result)
			
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
@transaction.atomic()	
def product_sku_manage(request,id=None):
	result = {}
	result['success'] = False
	result['message'] = ''
	
	#先找出商品
	try:
		product = Product.objects.get(id=id)
	except Exception as err:
		logger.error('Can not find product which id is %s.' % id)
		result['message'] = _('商品找不到，可能商品已经被删除了，请重试。')
		return JsonResponse(result)
	
	if request.method == 'POST':
		attribute_id_list = request.POST.getlist("attribute-id")
		logger.debug("attribute_id_list:%s"  % attribute_id_list)
		#获取分组情况
		group_id_list = Attribute.objects.filter(id__in=attribute_id_list).values("group").distinct()
		
		logger.debug("group_id_list:%s" % group_id_list)
		#group_id_list = list(set(group_id_list))
		#按照分组，将属性分组形成多个list
		group = []
		for group_id in group_id_list:
			group.append(Attribute.objects.filter(id__in=attribute_id_list).filter(group__id=group_id['group'])) 
		
		#生成全量的sku
		sku = []
		list_before = []
		deal_attribute(list_before,group,0,len(group_id_list),sku)
		logger.debug("sku%s"%sku)
		#生成product_attribute
		
		#先取得已经有的product_attribute
		try:
			pa_list = Product_Attribute.objects.filter(product=product)
		except Exception as err:
			logger.error("error:%s" % err)
			pa_list = []
		
		logger.debug("pa_list:" + str(pa_list))
		
		sub_item_number = 0
		for sku_item in sku:
			sub_item_number += 1
			
			is_exist = False
			for pa in pa_list:
				#logger.debug("1:" + str(set(pa.attribute.all())))
				#logger.debug("2:" + str(set(sku_item)))
			
				delta = set(pa.attribute.all()) - set(sku_item)
				if len(delta)==0:
					is_exist = True
					break;
			
			if not is_exist:
				pa = Product_Attribute.objects.create(product=product,sub_item_number=str(sub_item_number),quantity=0,price_adjusment=0.0,image=None,min_order_quantity=1)
				pa.attribute = sku_item
				pa.save()
		
		result['success'] = True
		result['message'] = '成功'
		
		return JsonResponse(result)
		
		
@staff_member_required
@transaction.atomic()	
def product_sku_delete(request,method='delete',id=None):
	result = {}
	result['success'] = False
	result['message'] = ''
	
	if request.method == 'GET':
		if method == 'delete':
			try:
				sku = Product_Attribute.objects.get(id=id)
				sku.delete()
				
				result['success'] = True
				result['message'] = 'SKU删除成功'
				
			except Exception as err:
				logger.error("Delete sku failed. \n Error message:%s" % err)
				result['message'] = 'SKU删除失败，请重试。'
				return JsonResponse(result)
		elif method == 'clear':
			try:
				product = Product.objects.get(id=id)
			except Exception as err:
				product = None
				logger.error("Can not find product [%s] \n Error message:%s" % (id,err))
				result['message'] = '清除SKU删除失败，商品不存在或已被删除。'
				return JsonResponse(result)
				
			if product:
				for sku in product.attributes.all():
					sku.delete()
				product.save()
			
			result['success'] = True
			result['message'] = '清除SKU成功'
		
		return JsonResponse(result)		
		
@staff_member_required
@transaction.atomic()	
def product_sku_attribute_manage(request):		
	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = ''
	
	if request.method == 'POST':
		pa_id_list = request.POST.getlist("pa_id")
		logger.debug("ids:%s" % pa_id_list)
		
		for pa_id in pa_id_list:
			pa = Product_Attribute.objects.get(id=pa_id)
			pa.sub_item_number = request.POST.get('pa-sub_item_number-%s' % pa_id)
			pa.quantity = request.POST.get('pa-quantity-%s' % pa_id)
			#pa.price_adjusment = request.POST.get('pa-price_adjusment-%s' % pa_id)
			#pa.min_order_quantity = request.POST.get('pa-min_order_quantity-%s' % pa_id)
			pa.save()
			logger.debug("pa.quantity:%s" % pa.quantity)
	
	result_dict['success'] = True
	result_dict['message'] = '成功'
	return JsonResponse(result_dict)
		
		

#递归进行sku的计算		
def deal_attribute(list_before,group,level,all_level,sku):
	#logger.debug("进入函数，现在的情况，level：%s,\n sku:%s" % (level,sku))
	for item in group[level]:
		logger.debug("level:%s  item:%s  all_level:%s" % (level,item,all_level))
		tmp_list = [item]
		tmp_list += list_before

		if level < all_level - 1:
			#list_before.append(item)
			level_t = level + 1
			logger.debug("level:%s" % level_t)
			deal_attribute(tmp_list,group,level_t,all_level,sku)
		else:
			logger.debug("tmp_list%s"%tmp_list)
			sku.append(tmp_list)
		#logger.debug("sku%s"%sku)

		
@staff_member_required
@transaction.atomic()		
def product_picture_manage(request):
	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = ''
	
	if request.method == 'POST':
		#先找出商品
		try:
			product = Product.objects.get(id=request.POST.get('id'))
		except Exception as err:
			logger.error('Can not find product which id is %s.' % id)
			result['message'] = _('商品找不到，可能商品已经被删除了，请重试。')
			return JsonResponse(result)
		
		
		#保存主图和缩略图
		image_url = request.POST.get('product_image')
		product.image = image_url
		dot_index = image_url.rfind('.')
		thumb_url = image_url[:dot_index] + "-thumb" + image_url[dot_index:]
		logger.debug("thumb_url:%s" % thumb_url)
		product.thumb = thumb_url
		product.save()
		
		#保存sku图
		#找出所有SKU
		sku_list = product.attributes.all()
		for sku in sku_list:
			sku_image_id = request.POST.get('sku_image_%s' % sku.id,'')
			if sku_image_id:
				try:
					image = Product_Images.objects.get(id=sku_image_id)
					sku.image = image
					sku.save()
				except Exception as err:
					logger.error('Can not find sku_image in product_images. \n Error message:%s'%err)
		
		result_dict['success'] = True
		result_dict['message'] = '成功'
	
	return JsonResponse(result_dict)
		
		
@staff_member_required
def oper(request):	
	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = ''

	if request.method == 'POST':
		method = request.POST['method']
		logger.debug("Product batch method : %s " % method)
		oper_ids = request.POST.getlist('is_oper')
		logger.debug("oper_ids:%s" % oper_ids)
		if oper_ids == '':
			raise Http404
		else:
			#oper_id_list = oper_ids.split(',')
		
			if method == 'delete':
				for id in oper_ids:
					try:
						product = Product.objects.get(id=id)
						product.delete()
					except:
						logger.info('Can not find product which id is %s to delete.' % (id))
				result_dict['success'] = True
				result_dict['message'] = '产品批量删除成功'
						
			elif method == 'onpublish' or method == 'offpublish':
				for id in oper_ids:
					try:
						product = Product.objects.get(id=id)
						if method == 'onpublish':
							product.is_publish = True
						else:
							product.is_publish = False
						product.save()
					except:
						logger.info('Can not find product which id is %s to delete.' % (id))
				
				result_dict['success'] = True
				result_dict['message'] = '产品上下架状态设置成功'
				
			elif method == 'sort':
				for id in oper_ids:
					try:
						product = Product.objects.get(id=id)
						product.sort_order = request.POST.get('sort_%s' % id , '0' )
						product.save()
					except Exception as err:
						logger.error(err)
						logger.info('Can not find product which id is %s to set order.' % (id))
				result_dict['success'] = True
				result_dict['message'] = '产品顺序号设置成功'
		return JsonResponse(result_dict)
				
	else:
		raise Http404		
		

@staff_member_required
def product_list(request):
	ctx = {}
	
	if request.method == 'GET':
		
		#name_condition = request.GET.get('name','')
		#item_number_condition = request.GET.get('item_number','')
		
		query_item = request.GET.get('query_item','')
		item_value = request.GET.get('item_value','')
		
		from django.db.models import Q
		if query_item == 'item_name':
			product_list = Product.objects.filter(Q(name__icontains=item_value)).order_by('update_time').reverse()
		elif query_item == 'item_number':
			product_list = Product.objects.filter(Q(item_number__icontains=item_value)).order_by('update_time').reverse()
		else:
			product_list = Product.objects.all().order_by('update_time').reverse()
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
		ctx['query_item'] = query_item
		ctx['item_value'] = item_value
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/product_list_content.html',ctx)
	else:
			raise Http404
	
		
		
@staff_member_required
def product_make_static(request):
	ctx = {}
	ctx['product_list'] = Product.objects.all()
	return TemplateResponse(request,'admin/product/make_static.html',ctx)
	
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