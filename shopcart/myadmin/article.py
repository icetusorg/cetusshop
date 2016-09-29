#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Article,System_Config,Album
from shopcart.forms import article_basic_info_form
from shopcart.utils import System_Para,my_pagination,get_serial_number,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
import logging
logger = logging.getLogger('icetus.shopcart')

def get_page_size():
	try:
		size = System_Config.objects.get(name='admin_article_list_page_size').val
	except:
		logger.info('"admin_order_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size

@staff_member_required
@transaction.atomic()
def article_make_static(request):
	ctx = {}
	ctx['article_list'] = Article.objects.all()
	return render(request,'admin/article/make_static.html',ctx)

@staff_member_required
@transaction.atomic()
def delete(request):
	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = '表单填写的内容不合法，请检查。'
	if request.method == 'POST':
		article_id_list = request.POST.getlist('article_id',[])
		count = 0
		if article_id_list:
			for id in article_id_list:
				article = Article.objects.get(id=id)
				article.delete()
				count += 1
			result_dict['success'] = True
			result_dict['message'] = '%s 篇文章被成功删除' % count
		else:
			result_dict['message'] = '没有选择任何文章进行操作。'
	return JsonResponse(result_dict)

	
@staff_member_required
@transaction.atomic()	
def detail(request,id):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '文章管理'
	
	if request.method == 'GET':
		try:
			article = Article.objects.get(id=id)
			ctx['article'] = article
			return render(request,System_Config.get_template_name('admin') + '/article_detail.html',ctx)
		except Exception as err:
			logger.error("Can not find artice which id is %s . \n Error message: %s" % (id,err))
			raise Http404
	else:
		raise Http404	
	

@staff_member_required
def article_basic_edit(request):
	ctx = {}
	ctx['system_para'] = System_Para.get_default_system_parameters()
	
	result = {}
	result['success'] = False
	result['message'] = ''
	result['data'] = {}
	
	#加载自定义模板供选择
	from .file import file_list
	template_list = file_list(System_Config.get_template_name('client') + '/custmize/','custmize_template_article')
	logger.debug('custome_templates: %s' % template_list)
	ctx['custmize_template'] = template_list
		
	if request.method == 'GET':
		id = request.GET.get('id','')
		if id != '':
			try:
				article = Article.objects.get(id=id)
				ctx['article'] = article
				
				#图片处理URL
				ctx['action_url'] = '/admin/file-upload/article/%s/' % id
				logger.debug('action_url:%s' % ctx['action_url'])
				
				ctx['file_delete_url'] = '/file-delete/article'
					
				
				try:
					ctx['image_list'] = Album.objects.filter(item_type='article').filter(item_id=id).order_by('create_time').reverse()
					logger.debug("ctx['image_list']:%s" % ctx['image_list'])
				except Exception as err:
					logger.error("Error:%s" % err)
					ctx['image_list'] = []
				
				
			except Exception as err:
				logger.error('Can not find article which id is %s. The error message is %s' % (id,err))
		return render(request,System_Config.get_template_name('admin') + '/article_detail.html',ctx)
	elif request.method == 'POST':
		try:
			article = Article.objects.get(id=request.POST['id'])
			form = article_basic_info_form(request.POST,instance=article)
		except:
			form = article_basic_info_form(request.POST)
			logger.info('New product to store.')
		
		if form.is_valid():
			article = form.save()
			result['success'] = True
			result['message'] = '文章保存成功'
			data = {}
			data['article_id'] = article.id
			result['data'] = data
		else:
			result['success'] = False
			result['message'] = '文章保存失败'
			result['data'] = {}
		return JsonResponse(result)
	else:
		raise Http404	

	
	
@staff_member_required
@transaction.atomic()	
def list_view(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['page_name'] = '文章管理'
	
	if request.method == 'GET':
		title = request.GET.get('title','')
		ctx['title'] = title
		type = request.GET.get('type','')
		ctx['type'] = type
		
		all = Article.objects.all()
				
		if title:
			from django.db.models import Q
			all = all.filter(Q(title__icontains=title))
		
		if type:
			all = all.filter(category=type)
			
		page_size = get_page_size()
		artile_list, page_range = my_pagination(request=request, queryset=all,display_amount=page_size)
		
		ctx['article_list'] = artile_list
		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['article_count'] = all.count()
		return render(request,System_Config.get_template_name('admin') + '/article_list.html',ctx)
	else:
		raise Http404
	