#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Article,System_Config
from shopcart.utils import System_Para,handle_uploaded_file
from django.http import Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

@staff_member_required
def article_make_static(request):
	ctx = {}
	ctx['article_list'] = Article.objects.all()
	return render(request,'admin/article/make_static.html',ctx)
	