# coding=utf-8
from django.shortcuts import render, redirect
from shopcart.models import Article, System_Config, Album, ArticleBusiCategory, Recruit
from shopcart.forms import recruit_basic_info_form
from shopcart.utils import my_pagination, get_serial_number, get_system_parameters
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.template.response import TemplateResponse
import logging

logger = logging.getLogger('icetus.shopcart')


def get_page_size():
    try:
        size = System_Config.objects.get(name='admin_article_list_page_size').val
    except:
        logger.info('"admin_order_list_page_size" is not setted.Use default value 8.')
        size = 8
    return size

def detail(request, id):
    ctx = {}
    ctx['system_para'] = get_system_parameters()


    if request.method == 'GET':
        try:
            try:
                recruit = Recruit.objects.get(id=id)
                ctx['recruit'] = recruit
                ctx['page_name'] = recruit.title
            except Exception as err:
                logger.error('找不到编号为 %s 。' % [id, ])
                raise Http404


            return TemplateResponse(request, System_Config.get_template_name() + '/recruit_detail.html', ctx)
        except Exception as err:
            logger.error("Can not find artice which id is %s . \n Error message: %s" % (id, err))
            raise Http404
    else:
        raise Http404

def view_list_view(request):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    if request.method == 'GET':

        all = Recruit.objects.all().order_by('-sort_order')

        page_size = get_page_size()

        # count = len(all)
        recruit_list, page_range, current_page = my_pagination(request=request, queryset=all, display_amount=page_size)
        logger.debug('current_page:%s' % current_page)

        # 为页面准备分类的下拉列表
        # from shopcart.myadmin.article_busi_category import get_all_category
        # busi_category_list = get_all_category()
        # logger.debug('busi_category_list : %s' % busi_category_list)
        # ctx['busi_category_list'] = busi_category_list

        ctx['recruit_list'] = recruit_list
        ctx['page_range'] = page_range
        ctx['page_size'] = page_size
        ctx['current_page'] = current_page
        # ctx['article_count'] = count
        logger.debug('正常访问招聘页面' + System_Config.get_template_name())
        return TemplateResponse(request, System_Config.get_template_name() + '/recruit_list.html', ctx)
    else:
        raise Http404

