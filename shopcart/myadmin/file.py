#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Product,System_Config,Product_Images,Album,Article,Attribute,Attribute_Group,Slider
from shopcart.forms import product_add_form
from shopcart.utils import handle_uploaded_file,my_pagination
from django.http import Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
import json
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

@staff_member_required
@csrf_exempt
def file_list_show(request,item_type,item_id):
	ctx = {}
	ctx['action_url'] = '/admin/file-upload/' + item_type + '/' + item_id + "/"
	ctx['file_delete_url'] = '/file-delete/' + item_type
	ctx['host_item_id'] = item_id
	ctx['item_type'] = item_type
	if request.method == 'GET':
		if item_type == 'product' or item_type == 'product_album':
			try:
				item = Product.objects.get(id=item_id)
				ctx['item'] = item
				try:
					image_list = Product_Images.objects.filter(product=item).order_by('create_time').reverse()
					if item_type == 'product_album':
						image_list = Album.objects.filter(item_type=item_type,item_id=item.id).order_by('create_time').reverse()
				except:
					image_list = []
			except:
				raise Http404
		elif item_type == 'article':
			try:
				item = Article.objects.get(id=item_id)
				ctx['item'] = item
				try:
					image_list = Album.objects.filter(item_type=item_type,item_id=item.id).order_by('create_time').reverse()
				except:
					image_list = []
			except:
				raise Http404
		elif item_type == 'attribute':
			try:
				item = Attribute_Group.objects.get(id=item_id)
				ctx['item'] = item
				try:
					image_list = Album.objects.filter(item_type=item_type,item_id=item.id).order_by('create_time').reverse()
				except:
					image_list = []
			except:
				raise Http404
		elif item_type == 'slider':
			try:
				item = Slider.objects.get(id=item_id)
				ctx['item'] = item
				try:
					image_list = Album.objects.filter(item_type=item_type,item_id=item.id).order_by('create_time').reverse()
				except:
					image_list = []
			except:
				raise Http404
		else:
			raise Http404
			
		page_size = 12
		count = image_list.count()
		image_list, page_range,current_page = my_pagination(request=request, queryset=image_list,display_amount=page_size)	
		ctx['image_list'] = image_list	
		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['current_page'] = current_page
		ctx['item_count'] = count
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/picture_list.html',ctx)
	else:
		raise Http404



	
@staff_member_required
@csrf_exempt
def file_upload(request,item_type,item_id):
	ctx = {}
	ctx['action_url'] = '/admin/file-upload/' + item_type + '/' + item_id + "/"
	ctx['file_delete_url'] = '/file-delete/' + item_type
	ctx['host_item_id'] = item_id
	
	if request.method == 'GET':
		ctx['item_type'] = item_type
		ctx['extra_info'] = request.GET.get('extra-info')
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/file_upload.html',ctx)
	else:
		ctx['result_message'] = '文件上传成功'
		
		
		result_extra = {}
		ctx['result_extra'] = json.dumps(result_extra)
		
		manual_name = request.POST.get('manual_name','noname')	
		same_name_handle = request.POST.get('same_name_handle','reject')
		alt_value = request.POST.get('alt_value','')
		filename_type = request.POST.get('filename_type','random')
		href = request.POST.get('href','')
		sort = request.POST.get('sort','0')
		extra_info = request.POST.get('extra_info','')
	
		if item_type == 'product' or item_type == 'product_album':
			try:
				item = Product.objects.get(id=item_id)
			except:
				raise Http404
			

			logger.debug("filename_type:%s" % filename_type)
			filenames = handle_uploaded_file(request.FILES['upload'],item_type,item_id,filename_type,manual_name,same_name_handle)
			if filenames['upload_result'] == False:
				ctx['result_message'] = filenames['upload_error_msg']
				return TemplateResponse(request,System_Config.get_template_name('admin') + '/file_upload.html',ctx)
				#return HttpResponse(filenames['upload_error_msg'])
			
			real_name = filenames['real_name']
			thumb_name = filenames['real_thumb']
			file_path = filenames['real_path']
			
			#加入到对象的图片列表中去
			is_show = request.POST.get('is_show_in_product_detail',False)
			
			if item_type == 'product':
				pi = Product_Images.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],product=item,sort=sort,is_show_in_product_detail=is_show,alt_value=alt_value,file_name=real_name,thumb_name = thumb_name,path=file_path)
				'''
				如果改商品原来没有图片，则自动把第一张作为主图
				'''
				if not item.image:
					item.image = pi.image
					item.thumb = pi.thumb
					item.save()
					
				result_extra['img_id'] = pi.id	
			else:
				ai = Album.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],item_type=item_type,item_id=item.id,alt_value=alt_value,file_name=real_name,thumb_name = thumb_name,sort=sort,path=file_path)
				
				result_extra['img_id'] = ai.id
		elif item_type == 'article':
			try:
				item = Article.objects.get(id=item_id)
			except:
				raise Http404
			filenames = handle_uploaded_file(request.FILES['upload'],item_type,item_id,filename_type,manual_name,same_name_handle)
			if filenames['upload_result'] == False:
				ctx['result_message'] = filenames['upload_error_msg']
				return TemplateResponse(request,System_Config.get_template_name('admin') + '/file_upload.html',ctx)				
		
			real_name = filenames['real_name']
			thumb_name = filenames['real_thumb']
			file_path = filenames['real_path']
		
			logger.debug('Upload success!!!')
			ai = Album.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],item_type=item_type,item_id=item.id,alt_value=alt_value,file_name=real_name,thumb_name = thumb_name,sort=sort,path=file_path)
			'''
			如果改文章原来没有图片，则自动把第一张作为主图
			'''
			if not item.image:
				item.image = ai.image
				item.thumb = ai.thumb
				item.save()
			result_extra['img_id'] = ai.id
			logger.debug('ai success!!!')
			
		elif item_type == 'attribute':
			try:
				item = Attribute_Group.objects.get(id=item_id)
			except:
				raise Http404
			filenames = handle_uploaded_file(request.FILES['upload'],item_type,item_id,request.POST['filename_type'],manual_name,same_name_handle)
			if filenames['upload_result'] == False:
				ctx['result_message'] = filenames['upload_error_msg']
				return TemplateResponse(request,System_Config.get_template_name('admin') + '/file_upload.html',ctx)
			
			real_name = filenames['real_name']
			thumb_name = filenames['real_thumb']
			file_path = filenames['real_path']
			
			ai = Album.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],item_type=item_type,item_id=item.id,alt_value=alt_value,file_name=real_name,thumb_name = thumb_name,sort=sort,path=file_path)
			result_extra['img_id'] = ai.id
			logger.info('Attribute_Group image upload success')
		elif item_type == 'slider':
			try:
				item = Slider.objects.get(id=item_id)
			except:
				raise Http404
			filenames = handle_uploaded_file(request.FILES['upload'],item_type,item_id,request.POST['filename_type'],manual_name,same_name_handle)
			if filenames['upload_result'] == False:
				ctx['result_message'] = filenames['upload_error_msg']
				return TemplateResponse(request,System_Config.get_template_name('admin') + '/file_upload.html',ctx)
			
			real_name = filenames['real_name']
			thumb_name = filenames['real_thumb']
			file_path = filenames['real_path']
			
			ai = Album.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],item_type=item_type,item_id=item.id,alt_value=alt_value,href=href,file_name=real_name,thumb_name = thumb_name,sort=sort,path=file_path)
			result_extra['img_id'] = ai.id
			logger.info('Slider image upload success')	
		
		else:
			raise Http404
			
		logger.info('come in')	
		#判断是否是从CKEDITER传上来的
		if 'CKEditorFuncNum' in request.GET:
			logger.debug('请求来自CKEDITER.')
			script = '<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction("' + request.GET['CKEditorFuncNum'] + '","' + filenames['image_url'] + '");</script>';
			logger.debug('返回的script： %s' % [script])
			return HttpResponse(script,content_type='text/html;charset=UTF-8')
			
		return_url = '/admin/file-upload/' + item_type + '/' + item_id + "/"
		if 'return_url' in request.POST:
			return_url = request.POST.get('return_url')
			return redirect(return_url)
			
		result_extra['extra_info'] = extra_info	
		ctx['result_extra'] = json.dumps(result_extra)
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/file_upload.html',ctx)
		
		

@staff_member_required
def file_delete(request,item_type,item_id,host_item_id):
	ctx = {}
	ctx['file_delete_url'] = '/file-delete/' + item_type
	if request.method == 'GET':
		try:
			if item_type == 'product':
				image = Product_Images.objects.get(id=item_id)
				image.delete()
			elif item_type == 'product_album':
				image = Album.objects.get(id=item_id)
				image.delete()
			elif item_type == 'article':
				image = Album.objects.get(id=item_id)
				image.delete()
			else:
				raise Http404
		except:
			raise Http404
		
		redirect_url = '/admin/file-upload/' + item_type + '/' + host_item_id + "/"
		if 'return_url' in request.GET:
			redirect_url = request.GET.get('return_url')
		
		return redirect(redirect_url)
		

def file_list(path,filetype):
	import os
	if filetype == 'custmize_template_product':
		path = 'shopcart/templates/' + path + 'product/'
	elif filetype == 'custmize_template_article':
		path = 'shopcart/templates/' + path + 'article/'
	elif filetype == 'custmize_template_category':
		path = 'shopcart/templates/' + path + 'category/'
	elif filetype == 'custmize_template_article_category':
		path = 'shopcart/templates/' + path + 'article_category/'
	else:
		pass
	
	logger.debug('Looking path: %s' % path)
	if os.path.exists(path):
		if os.path.isdir(path):
			return os.listdir(path)
	
	return []
		
		
@staff_member_required
def ckediter(request,item_type,item_id):
	ctx = {}
	ctx['upload_url'] = '/admin/file-upload/' + item_type + '/' + item_id + '/'
	ctx['article_content'] = ''
	ctx['id'] = item_id
	if request.method == 'GET':
		try:
			if item_type == 'product':
				ctx['article_content'] = Product.objects.get(id=item_id).description
			elif item_type == 'article':
				ctx['article_content'] = Article.objects.get(id=item_id).content
			else:
				raise Http404
		except:
			raise Http404
		return TemplateResponse(request,'admin/ckediter.html',ctx)

		
		
@staff_member_required
def space_count(request):
	ctx = {}
	if request.method == 'GET':
		from shopcart.utils import count_file_size
		path = 'media/'
		size = count_file_size(path)
		return HttpResponse('%s 字节' % size)	