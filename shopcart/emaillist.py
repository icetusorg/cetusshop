#coding=utf-8
from django.shortcuts import render,redirect
from shopcart.models import Email_List
from django.core.context_processors import csrf
from django.http import HttpResponse,JsonResponse
import json,uuid
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

def add_to_email_list(request):
	email = json.loads((request.body).decode())
	result_dict = {}
	try:
		email_list,create = Email_List.objects.get_or_create(email=email['email'].lower())
		result_dict['success'] = True
		result_dict['message'] = _('Add email to email list success')
	except Exception as err:
		logger.error('Add email which %s to email list failed. Cause by:%s' % (email['email'],err))
		result_dict['success'] = False
		result_dict['message'] = _('Add email to email list failed')
	return JsonResponse(result_dict)

