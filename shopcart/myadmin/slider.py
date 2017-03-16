#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import System_Config,Album,Slider
from shopcart.utils import my_pagination,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart.forms import express_form,express_type_form
import logging
logger = logging.getLogger('icetus.shopcart')

	
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
				picture.delete()
				result['success'] = True
				result['message'] = '幻灯图片信息删除成功'
			else:
				result['message'] = '幻灯图片信息删除失败，可能图片已经被删除了。'
			
			return JsonResponse(result)
	else:
		raise Http404	
	
