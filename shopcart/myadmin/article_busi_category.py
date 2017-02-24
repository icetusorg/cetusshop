#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import ArticleBusiCategory,System_Config
from shopcart.utils import System_Para,my_pagination,get_serial_number,get_system_parameters
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
import logging
logger = logging.getLogger('icetus.shopcart')

def get_all_category():
	return ArticleBusiCategory.objects.all()
	

	
