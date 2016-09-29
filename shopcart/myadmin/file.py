#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Product,System_Config,Product_Images,Album,Article
from shopcart.forms import product_add_form
from shopcart.utils import System_Para,handle_uploaded_file
from django.http import Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

	
@staff_member_required
@csrf_exempt
def file_upload(request,item_type,item_id):
	ctx = {}
	ctx['system_para'] = System_Para.get_default_system_parameters()
	ctx['action_url'] = '/admin/file-upload/' + item_type + '/' + item_id + "/"
	ctx['file_delete_url'] = '/file-delete/' + item_type
	ctx['host_item_id'] = item_id
	if request.method == 'GET':
		if item_type == 'product' or item_type == 'product_album':
			try:
				item = Product.objects.get(id=item_id)
				ctx['item'] = item
				try:
					ctx['image_list'] = Product_Images.objects.filter(product=item).order_by('create_time').reverse()
					if item_type == 'product_album':
						ctx['image_list'] = Album.objects.filter(item_type=item_type,item_id=item.id).order_by('create_time').reverse()
				except:
					ctx['image_list'] = []
			except:
				raise Http404
		elif item_type == 'article':
			try:
				item = Article.objects.get(id=item_id)
				ctx['item'] = item
				try:
					ctx['image_list'] = Album.objects.filter(item_type=item_type,item_id=item.id).order_by('create_time').reverse()
				except:
					ctx['image_list'] = []
			except:
				raise Http404
		else:
			raise Http404
		return render(request,'admin/file_upload.html',ctx)
	else:
		
		manual_name = request.POST.get('manual_name','noname')	
		same_name_handle = request.POST.get('same_name_handle','reject')
	
		if item_type == 'product' or item_type == 'product_album':
			try:
				item = Product.objects.get(id=item_id)
			except:
				raise Http404
			

			logger.debug("filename_type:%s" % request.POST['filename_type'])
			filenames = handle_uploaded_file(request.FILES['upload'],item_type,item_id,request.POST['filename_type'],manual_name,same_name_handle)
			if filenames['upload_result'] == False:
				return HttpResponse(filenames['upload_error_msg'])
				
			#加入到对象的图片列表中去
			sort = request.POST.get('sort','0')
			is_show = request.POST.get('is_show_in_product_detail',False)
			
			if item_type == 'product':
				pi = Product_Images.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],product=item,sort=sort,is_show_in_product_detail=is_show)
			else:
				ai = Album.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],item_type=item_type,item_id=item.id)
		elif item_type == 'article':
			try:
				item = Article.objects.get(id=item_id)
			except:
				raise Http404
			filenames = handle_uploaded_file(request.FILES['upload'],item_type,item_id,request.POST['filename_type'],manual_name,same_name_handle)
			if filenames['upload_result'] == False:
				return HttpResponse(filenames['upload_error_msg'])			
		
			logger.debug('Upload success!!!')
			ai = Album.objects.create(image=filenames['image_url'],thumb=filenames['thumb_url'],item_type=item_type,item_id=item.id)
			logger.debug('ai success!!!')
		else:
			raise Http404
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
		
@staff_member_required
def file_delete(request,item_type,item_id,host_item_id):
	ctx = {}
	ctx['system_para'] = System_Para.get_default_system_parameters()
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
	ctx['system_para'] = System_Para.get_default_system_parameters()
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
		return render(request,'admin/ckediter.html',ctx)
