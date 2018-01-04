from django.shortcuts import render, redirect
from shopcart.models import Category, System_Config, Menu
from shopcart.utils import my_pagination, get_serial_number, get_system_parameters
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from shopcart import category as category_util
from shopcart.forms import menu_form, menu_simple_form
from django.template.response import TemplateResponse
import logging

logger = logging.getLogger('icetus.shopcart')


def get_all_menu():
    menu_list = Menu.objects.all()
    return menu_list


def get_all_top_menu():
    top_menu_list = Menu.objects.filter(parent=None)
    return top_menu_list


@staff_member_required
@transaction.atomic()
def list_view(request):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = '菜单管理'

    if request.method == 'GET':
        title = request.GET.get('title', '')
        ctx['title'] = title

        top_menu_list = get_all_top_menu()

        ctx['menu_list'] = top_menu_list

        return TemplateResponse(request, System_Config.get_template_name('admin') + '/edit_menu.html', ctx)
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def ajax_add_menu(request):
    if request.method == 'POST':
        result = {}
        result['success'] = False
        result['message'] = '菜单信息保存失败'
        form = menu_simple_form(request.POST)
        if form.is_valid():
            menu = form.save()
            parent_id = request.POST.get('parent_id', '')
            if parent_id != '':
                try:
                    parent = Menu.objects.get(id=parent_id)
                    menu.parent = parent
                    menu.save()
                except Exception as err:
                    logger.info('Can not find category which id is [%s]. Create one. \n Error Message: %s' % (id, err))
                    return JsonResponse(result)

            result['success'] = True
            result['message'] = '菜单信息保存成功'
            result['menu_id'] = menu.id

        return JsonResponse(result)
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def edit(request, id):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = '菜单管理'

    if request.method == 'POST':
        result = {}
        result['success'] = False
        result['message'] = '菜单信息保存失败'

        menu = None
        try:
            menu = Menu.objects.get(id=id)
        except Exception as err:
            logger.info('Can not find category which id is [%s]. Create one. \n Error Message: %s' % (id, err))

        if menu:
            form = menu_form(request.POST, instance=menu)
        else:
            form = menu_form(request.POST)
        # form = category_simple_form(request.POST)

        logger.debug('name:' + request.POST.get('name'))

        if form.is_valid():
            category = form.save()
            result['success'] = True
            result['message'] = '菜单信息保存成功'
            result['category_id'] = category.id
        else:
            logger.debug('form not valid')

        return JsonResponse(result)

    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def sort(request):
    if request.method == 'POST':
        result = {}
        id_list = request.POST.getlist('selected')
        logger.error('id_list %s' % id_list)
        for id in id_list:
            try:
                menu = Menu.objects.get(id=id)
            except Exception as err:
                logger.error('Can not find menu %s .\n Error Message: %s' % (id, err))
                menu = None
            if menu:
                try:
                    sort = request.POST.get('sort_%s' % id)
                except:
                    sort = None
                if sort:
                    menu.sort_order = sort
                    menu.save()
        result['success'] = True
        result['message'] = '菜单排序保存成功'

        return JsonResponse(result)
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def delete(request, id):
    if request.method == 'POST':
        result = {}
        result['success'] = False
        result['message'] = '菜单信息删除失败'
        logger.info('进入菜单删除')
        try:
            menu = Menu.objects.get(id=id)
            logger.info('获取到删除菜单信息 %s' % menu.id)
        except Exception as err:
            logger.info('Can not find category which id is [%s]. Create one. \n Error Message: %s' % (id, err))
            return JsonResponse(result)

        # 判断category有没有子菜单
        sub_category_count = menu.childrens.all().count()
        logger.info('Category [%s] has [%s] sub_categorys.' % (menu.name, sub_category_count))
        if sub_category_count > 0:
            result['success'] = False
            result['message'] = '该菜单下存在子菜单，请先删除子菜单。'
            return JsonResponse(result)

        menu.delete()
        result['success'] = True
        result['message'] = '菜单信息删除成功'

        return JsonResponse(result)

    else:
        raise Http404
