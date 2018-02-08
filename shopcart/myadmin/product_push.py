# coding=utf-8
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from shopcart.models import System_Config, ProductPush, ProductPushGroup, Product
from shopcart.utils import my_pagination
from shopcart.forms import push_group_detail_form
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
import logging, json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from django.db import transaction
from shopcart.myadmin.utils import NO_PERMISSION_PAGE

import logging

logger = logging.getLogger('icetus.shopcart')


def get_page_size():
    try:
        size = System_Config.objects.get(name='admin_product_push_list_page_size').val
    except:
        logger.info('"admin_product_push_list_page_size" is not setted.Use default value 12.')
        size = 12
    return size


@staff_member_required
@transaction.atomic()
def list(request):
    ctx = {}
    ctx['page_name'] = '商品推荐管理'

    if request.method == 'GET':
        push_list = ProductPushGroup.objects.all().order_by('-create_time')

        logger.debug('push_list:%s' % push_list)

        count = push_list.count()
        page_size = get_page_size()
        push_list, page_range, current_page = my_pagination(request=request, queryset=push_list,
                                                            display_amount=page_size)

        ctx['page_range'] = page_range
        ctx['current_page'] = current_page
        ctx['page_size'] = page_size
        ctx['item_count'] = count

        ctx['push_list'] = push_list
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/product_push_list.html', ctx)
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def oper(request):
    if request.method == 'POST':
        result = {}
        method = request.GET.get('method', '')
        if method == 'set_relation':
            id = request.POST.get('host_id', '')
            try:
                push = ProductPushGroup.objects.get(id=id)
            except Exception as err:
                logger.error('Can not find push %s .\n Error Message: %s' % (id, err))
                result['success'] = False
                result['message'] = '保存推送商品相关信息失败，推送组找不到，可能已经被删除.'
                return JsonResponse(result)

            id_list = request.POST.getlist('is_oper')
            p_list = Product.objects.filter(id__in=id_list)

            for p in p_list:
                exit = False
                for exit_p in push.products.all():
                    logger.debug('exit_p:%s ---- p:%s' % (exit_p.product, p))
                    if exit_p.product == p:
                        logger.debug("exit:%s" % exit)
                        exit = True
                        break
                if not exit:
                    p_push = ProductPush.objects.create(product=p, group=push)
                    push.products.add(p_push)

            push.save()
            result['success'] = True
            result['message'] = '保存推送商品相关信息成功'
            return JsonResponse(result)
        elif method == 'delete':
            id = request.POST.get('id', '')
            try:
                push = ProductPushGroup.objects.get(id=id)
            except Exception as err:
                logger.error('Can not find push %s .\n Error Message: %s' % (id, err))
                result['success'] = False
                result['message'] = '推送商品组删除失败.'
                return JsonResponse(result)

            push.delete()
            result['success'] = True
            result['message'] = '推送商品组删除成功.'
            return JsonResponse(result)
        elif method == 'del_relation':
            id_list = request.POST.getlist('is_oper')

            push_list = ProductPush.objects.filter(id__in=id_list)
            for push in push_list:
                push.delete()

            result['success'] = True
            result['message'] = '推送商品信息删除成功.'
            return JsonResponse(result)
        elif method == 'save_content':
            id = request.POST.get('id', '')
            title = request.POST.get('title', '')
            sort_order = request.POST.get('sort_order', '')

            try:
                push = ProductPush.objects.get(id=id)
            except Exception as err:
                logger.error('Can not find push %s .\n Error Message: %s' % (id, err))
                result['success'] = False
                result['message'] = '保存推送商品信息失败.'
                return JsonResponse(result)

            push.title = title
            push.sort_order = sort_order
            push.save()
            result['success'] = True
            result['message'] = '保存推送商品信息成功.'
            return JsonResponse(result)

        else:
            raise Http404

    raise Http404


@staff_member_required
@transaction.atomic()
def detail(request):
    ctx = {}
    ctx['page_name'] = '商品推荐管理'
    if request.method == 'GET':
        id = request.GET.get('id', '')
        try:
            push = ProductPushGroup.objects.get(id=id)
        except Exception as err:
            push = None

        push_list = []
        if push:
            push_list = ProductPush.objects.filter(group=push)

        ctx['push_list'] = push_list
        ctx['push'] = push
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/product_push_detail.html', ctx)
    if request.method == 'POST':
        id = request.POST.get('id', '')
        result = {}
        try:
            push = ProductPushGroup.objects.get(id=id)
            form = push_group_detail_form(request.POST, instance=push)
        except Exception as err:
            push = None
            form = push_group_detail_form(request.POST)
        logger.info('监测点1')
        if form.is_valid():
            push = form.save()
        else:
            result['success'] = False
            result['message'] = '商品推荐组保存失败，请检查输入项。'
            return JsonResponse(result)

        result['success'] = True
        result['message'] = '商品推荐组保存成功。'
        data = {}
        data['push_group_id'] = push.id
        result['data'] = data
        return JsonResponse(result)
    else:
        raise Http404
