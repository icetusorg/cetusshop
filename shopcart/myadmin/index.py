# coding=utf-8
from django.shortcuts import render, redirect
from shopcart.models import System_Config, Order, Visitor, Product, Inquiry
from shopcart.utils import get_system_parameters
from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse
from django.db.models.aggregates import Count
from django.contrib.admin.views.decorators import staff_member_required
import logging

logger = logging.getLogger('icetus.shopcart')


@staff_member_required
def menu_view(request):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    return TemplateResponse(request, System_Config.get_template_name('admin') + '/menu.html', ctx)


@staff_member_required
def view(request):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    if request.method == 'GET':
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/index.html', ctx)


def heart(request):
    result = {}
    result['success'] = True
    return JsonResponse(result)


@staff_member_required
def content_view(request):
    from datetime import datetime, timedelta
    from shopcart.functions import date_time_util
    ctx = {}
    ctx['system_para'] = get_system_parameters()

    visitor_number = Visitor.objects.count()  # 获取访问数
    ctx['vistor'] = visitor_number
    visitor_day_num = Visitor.objects.filter(create_time__gt=date_time_util.get_day_of_day(-1 + 1)).filter(
        create_time__lt=date_time_util.get_day_of_day(0 + 1)).count() # 获取今天的访问数
    ctx['visitor_day_num'] = visitor_day_num

    maturity_data = System_Config.objects.get(name='maturity_data').val  # 获取到期时间
    ctx['maturity_data'] = maturity_data

    product_num = Product.objects.count()  # 获取产品总数
    ctx['product_num'] = product_num

    product_day_num = Product.objects.filter(create_time__gt=date_time_util.get_day_of_day(-1 + 1)).filter(
        create_time__lt=date_time_util.get_day_of_day(0 + 1)).count() # 获取今天的访问数  # 获取今天产品总数
    ctx['product_day_num'] = product_day_num

    inquiry_num = Inquiry.objects.count()  # 获取询盘总数
    ctx['inquiry_num'] = inquiry_num

    inquiry_day_num = Inquiry.objects.filter(create_time__gt=date_time_util.get_day_of_day(-1 + 1)).filter(
        create_time__lt=date_time_util.get_day_of_day(0 + 1)).count()  # 获取今天询盘总数
    ctx['inquiry_day_num'] = inquiry_day_num

    if request.method == 'GET':
        import datetime
        # start_date = datetime.date(2017, 3, 15)
        # end_date = datetime.date(2017, 3, 16)
        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        ctx['order_count_today'] = Order.objects.filter(create_time__gt=start).count()
        ctx['order_not_pay_count_today'] = Order.objects.filter(create_time__gt=start).filter(
            status=Order.ORDER_STATUS_PLACE_ORDER).count()
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/index_content.html', ctx)


def login(request):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    if request.method == 'GET':
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/login.html', ctx)


def no_permission(request):
    return HttpResponse('您没有相应的权限，请联系管理员分配。')
