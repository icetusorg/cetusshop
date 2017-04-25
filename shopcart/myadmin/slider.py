#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import System_Config,Album,Slider
from shopcart.utils import my_pagination
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart.forms import slider_detail_form
from django.template.response import TemplateResponse
import logging
logger = logging.getLogger('icetus.shopcart')


def get_page_size():
	try:
		size = System_Config.objects.get(name='admin_slider_list_page_size').val
	except:
		logger.info('"admin_slider_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size

	
@staff_member_required
@transaction.atomic()	
def set_image(request):

	if request.method == 'POST':
		result = {}
		result['success'] = False
		result['message'] = '幻灯图片信息保存失败'
		
		method = request.POST.get('method','')
		if method == 'delete':
			picture_id = request.POST.get('picture_id','')
			picture = None
			try:
				picture = Album.objects.get(id=picture_id)
			except Exception as err:
				logger.info('Can not find  picture [%s] in Album. \n Error Message: %s' %(picture_id,err))
			
			if picture:
				picture.remove_file()
				picture.delete()
				result['success'] = True
				result['message'] = '幻灯图片信息删除成功'
			else:
				result['message'] = '幻灯图片信息删除失败，可能图片已经被删除了。'
			
			return JsonResponse(result)
	else:
		raise Http404
		
@staff_member_required
@transaction.atomic()		
def edit(request):
	ctx = {}
	ctx['page_name'] = '幻灯片管理'

	if request.method == 'GET':
		id = request.GET.get('id','')
		try:
			slider = Slider.objects.get(id=id)
		except Exception as err:
			logger.info('Can not find  slider [%s] in Slider. \n Error Message: %s' %(id,err))
			slider = None
		ctx['slider'] = slider
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/slider_detail.html',ctx)
	elif request.method == 'POST':
		id = request.GET.get('id','')
		result = {}
		
		try:
			slider = Slider.objects.get(id=id)
			form = slider_detail_form(request.POST,instance=slider)
		except:
			slider = None
			form = slider_detail_form(request.POST)
			logger.info('New slider to store.')
		
		if form.is_valid():
			slider = form.save()
			
		result['success'] = True
		result['message'] = '幻灯片保存成功'
		data = {}
		data['slider_id'] = slider.id
		result['data'] = data	
		return JsonResponse(result)
		
	else:
		raise Http404
		
		
@staff_member_required
@transaction.atomic()		
def oper(request):
	ctx = {}
	ctx['page_name'] = '幻灯片删除'

	if request.method == 'POST':
		method = request.POST.get('method','')
		id = request.POST.get('id','')
		result = {}
		
		try:
			slider = Slider.objects.get(id=id)
		except Exception as err:
			slider = None
			logger.info('Can not find  slider [%s] in Slider. \n Error Message: %s' %(id,err))
			result['success'] = False
			result['message'] = '幻灯片删除失败，原幻灯片找不到，可能已经被删除。'
			return JsonResponse(result)
		
		if method == 'delete':
			if slider:
				slider.remove_file()
				slider.delete()
			
		result['success'] = True
		result['message'] = '幻灯片删除成功'
		return JsonResponse(result)
		
	else:
		raise Http404			
		

@staff_member_required
@transaction.atomic()		
def list(request):
	ctx = {}
	ctx['page_name'] = '幻灯片管理'

	if request.method == 'GET':
		slider_list = Slider.objects.order_by('-create_time')
	
		page_size = get_page_size()
		slider_list, page_range = my_pagination(request=request, queryset=slider_list,display_amount=page_size)	
		
		ctx['slider_list'] = slider_list
		ctx['page_range'] = page_range
		ctx['page_size'] = page_size
		ctx['item_count'] = Slider.objects.all().count()
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/slider_list.html',ctx)
	else:
		raise Http404	
