#coding=utf-8
from django.shortcuts import render
from django.template.loader import render_to_string
from shopcart.models import System_Config,Article,ArticleBusiCategory
from shopcart.utils import System_Para,my_pagination,get_system_parameters,customize_tdk
import json,os
from django.http import JsonResponse
from django.http import Http404
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

# Create your views here.
def detail(request,id):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Blog'
	try:
		article = Article.objects.get(id=id)
	except:
		raise Http404
		
	ctx['article'] = article
	if article.page_title:
		ctx['page_name'] = article.page_title
	else:
		ctx['page_name'] = article.title
	ctx['page_key_words'] = article.keywords
	ctx['page_description'] = article.short_desc
	
	template = '/article.html'
		
	if article.detail_template != '':
		if article.detail_template != 'USE_DEFAULT':
			template = '/custmize/article/' + article.detail_template	
	
	logger.info('The template name is %s' % template)
	
	if request.method =='GET': #正常访问，返回动态页面
		return render(request,System_Config.get_template_name() + template, ctx)
	elif request.method == 'POST':#通过ajax访问，生成静态文件
		content = render_to_string(System_Config.get_template_name() + template, ctx)
		result_dict = {}
		try:
			import codecs,os
			dir = 'www/' + article.folder
			dir_http = article.folder
			
			if not os.path.exists(dir):
				os.makedirs(dir)
				
			if not dir.endswith('/'):
				dir = dir + '/'
				
			if not dir_http.endswith('/'):
				dir_http = dir_http + '/'
			
			f = codecs.open(dir + article.static_file_name ,'w','utf-8')
			f.write(content)
			f.close()
			result_dict['success'] = True
			result_dict['message'] = _('File already generated.')
			result_dict['static_url'] = dir_http + article.static_file_name
		except Exception as err:
			logger.error('写文件失败。' + str(err))
			result_dict['success'] = False
			result_dict['message'] = _('File generate failed.')
		finally:
			if f is not None:
				f.close()
		return JsonResponse(result_dict)
		
def view_blog_list(request,category_id=None):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Blog'
	
	try:
		blog_list_page_size = System_Config.objects.get('blog_list_page_size')
	except:
		logger.debug('blog_list_page_size is not defined,use the default value 12.')
		blog_list_page_size = 12
	
	if request.method =='GET':	
		template = 'blog_list.html'
		if 'sort_by' in request.GET:
			if 'direction' in request.GET:
				if 'desc' == request.GET['direction']:
					article_list = Article.objects.filter(category=Article.ARTICLE_CATEGORY_BLOG).order_by(request.GET['sort_by']).reverse()
				else:
					article_list = Article.objects.filter(category=Article.ARTICLE_CATEGORY_BLOG).order_by(request.GET['sort_by'])
			else:
				article_list = Article.objects.filter(category=Article.ARTICLE_CATEGORY_BLOG).order_by(request.GET['sort_by'])
		else:
			article_list = Article.objects.filter(category=Article.ARTICLE_CATEGORY_BLOG)
			
			
		#按分类筛选
		logger.debug('category_id : %s ' % category_id)
		if category_id:
			#查找该分类是否设置了自定义的分类模板
			try:
				category = ArticleBusiCategory.objects.get(id=category_id)
				ctx['page_key_words'] = category.keywords
				ctx['page_description'] = category.short_desc
				if category.page_title:
					ctx['page_name'] = category.page_title
				else:
					ctx['page_name'] = category.name
					
				if category.category_template:
					template = '/custmize/article_category/' + category.category_template
				article_list = article_list.filter(busi_category=category)
			except Exception as err:
				logger.error('Can not find category which id is %s. Error message is %s ' % (category_id,err))
		
		if 'page_size' in request.GET:
			logger.debug('the page_size has been detacted')
			article_list, page_range = my_pagination(request=request, queryset=article_list,display_amount=request.GET['page_size'])
		else:
			article_list, page_range = my_pagination(request=request, queryset=article_list,display_amount=blog_list_page_size)
		
		ctx['article_list'] = article_list
		ctx['page_range'] = page_range
		logger.info('template : ' + template)
		return render(request,System_Config.get_template_name() + '/' + template,ctx)