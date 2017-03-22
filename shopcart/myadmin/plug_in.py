#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import System_Config
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import logging
logger = logging.getLogger('icetus.shopcart')



@staff_member_required	
def list(request):
	ctx = {}

	if request.method == 'GET':
		return TemplateResponse(request,System_Config.get_template_name('admin') + '/plug_list.html',ctx)
		
