from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.http import Http404, HttpResponse, JsonResponse
from shopcart.models import Product, System_Config, Category, Attribute, Attribute_Group, Product_Attribute
from django.views.decorators.csrf import csrf_exempt
import logging

# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


@staff_member_required
def album_list(request):
    ctx = {}
    if request.method == 'GET':

        return TemplateResponse(request, System_Config.get_template_name('admin') + '/album_list.html', ctx)
    else:
        raise Http404


@staff_member_required
@csrf_exempt
def album_model(request):
    ctx = {}
    if request.method == 'GET':
        logger.debug("------------------" )
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/album_message_input.html', ctx)
