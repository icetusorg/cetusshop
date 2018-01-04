# coding=utf-8
from django.shortcuts import render, redirect, render_to_response
from shopcart.models import System_Config, Inquiry_Products, Cart_Products, Inquiry
from shopcart.utils import get_system_parameters
from django.core.context_processors import csrf
from shopcart.forms import inquiry_form, email_inquiry_form
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext as _
from django.db import transaction
from django.http import Http404
from shopcart import signals
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from shopcart.functions.product_util_func import get_menu_products
from shopcart.utils import my_pagination, get_serial_number, get_system_parameters
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


# 基础询盘
@transaction.atomic()
def add(request):
    ctx = {}
    ctx.update(csrf(request))
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = 'Inquiry'

    result_dict = {}

    if request.method == 'POST':
        form = inquiry_form(request.POST)  # 获取Post表单数据

        code = request.POST.get('code', '')
        if code == request.session.get('check_code', 'error'):
            if form.is_valid():  # 验证表单
                inquiry = form.save()

                if inquiry.name == None or inquiry.name.strip() == '':
                    logger.info('Inquiry customer name is Null.')
                    inquiry.name = 'None'
                    # logger.debug('request.META:%s' % request.META)

                from .utils import get_remote_ip
                ip = get_remote_ip(request)
                inquiry.ip_address = ip
                type = request.POST.get('type', '')
                inquiry.type = type
                inquiry.save()

                result_dict['success'] = True
                result_dict['message'] = _(
                    'Your inquiry was submitted and will be responded to as soon as possible. Thank you for contacting us.')

                # 触发用户注册成功的事件
                signals.inquiry_received.send(sender='Inquiry', inquiry=inquiry)
            else:
                result_dict['success'] = False
                result_dict['message'] = _('Opration faild.')
        else:
            result_dict['message'] = _('Captcha Error')
        return JsonResponse(result_dict)


# 邮件订阅
@transaction.atomic()
def email_add(request):
    ctx = {}
    ctx.update(csrf(request))
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = 'Inquiry'

    result_dict = {}
    if request.method == 'POST':
        form = email_inquiry_form(request.POST)  # 获取Post表单数据

        if form.is_valid():  # 验证表单
            inquiry = form.save()
            if inquiry.email == None or inquiry.email.strip() == '':
                result_dict['success'] = False
                result_dict['message'] = _('Email faild.')
                return JsonResponse(result_dict)

            from .utils import get_remote_ip
            ip = get_remote_ip(request)
            type = request.POST.get('type', '')
            inquiry.type = type
            inquiry.ip_address = ip
            inquiry.save()

            result_dict['success'] = True
            result_dict['message'] = _(
                'Your inquiry was submitted and will be responded to as soon as possible. Thank you for contacting us.')

            # 触发用户注册成功的事件
            signals.inquiry_received.send(sender='Inquiry', inquiry=inquiry)
        else:
            result_dict['success'] = False
            result_dict['message'] = _('Opration faild.')
        return JsonResponse(result_dict)


# 购物车式询盘提交
@transaction.atomic()
def quote_add(request):
    ctx = {}
    ctx.update(csrf(request))
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = 'Quoted'

    result_dict = {}

    if request.method == 'POST':
        # 得到cart_product_id
        cart_product_id_list = request.POST.getlist('cart_product_id', [])
        logger.info('获取到的产品ID %s' % cart_product_id_list)
        form = inquiry_form(request.POST)  # 获取Post表单数据

        code = request.POST.get('code', '')

        if code == request.session.get('check_code', 'error'):
            if form.is_valid():  # 验证表单
                inquiry = form.save()
                if inquiry.name == None or inquiry.name.strip() == '':
                    logger.info('Inquiry customer name is Null.')
                    inquiry.name = 'None'
                    # logger.debug('request.META:%s' % request.META)

                from .utils import get_remote_ip
                ip = get_remote_ip(request)
                inquiry.ip_address = ip
                type = request.POST.get('type', '')
                inquiry.type = type
                # 向询盘加入商品
                for cp_id in cart_product_id_list:
                    cp = Cart_Products.objects.get(id=cp_id)
                    logger.debug('>>>>>:product.id=' + str(cp.product.id))
                    pa_id = None
                    pa_name = ''
                    pa_item_number = None

                    if cp.product_attribute:
                        pa_id = cp.product_attribute.id
                        pa_name = cp.product_attribute.get_grouped_attribute_desc()
                        pa_item_number = cp.product_attribute.sub_item_number
                    op = Inquiry_Products.objects.create(product_id=cp.product.id, product_attribute_id=pa_id,
                                                         inquiry=inquiry,
                                                         name=cp.product.name, short_desc=cp.product.short_desc,
                                                         item_number=cp.product.item_number,
                                                         thumb=cp.product.thumb, image=cp.product.image,
                                                         product_attribute_name=pa_name,
                                                         product_attribute_item_number=pa_item_number,
                                                         quantity=cp.quantity
                                                         )

                inquiry.save()

                result_dict['success'] = True
                result_dict['message'] = _(
                    'Your inquiry was submitted and will be responded to as soon as possible. Thank you for contacting us.')

                # 触发用户注册成功的事件
                signals.inquiry_received.send(sender='Inquiry', inquiry=inquiry)
            else:
                result_dict['success'] = False
                result_dict['message'] = _('Opration faild.')
        else:
            result_dict['message'] = _('Captcha Error')
        return JsonResponse(result_dict)


@login_required()
def show_order(request):
    logger.info('Start to show order.')
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['menu_products'] = get_menu_products()
    ctx['page_name'] = 'My Orders'
    if request.method == 'GET':
        inquiry_list = Inquiry.objects.filter(user=request.user)

        try:
            order_list_page_size = System_Config.objects.get('order_list_page_size')
        except:
            logger.debug('order_list_page_size is not defined,use the default value 10.')
            order_list_page_size = 10
        inquiry_list, page_range, current_page = my_pagination(request, inquiry_list,
                                                               display_amount=order_list_page_size)
        ctx['inquiry_list'] = inquiry_list
        ctx['page_range'] = page_range
        ctx['current_page'] = current_page
        return TemplateResponse(request, System_Config.get_template_name() + '/inquiry.html', ctx)


@login_required()
def inquiry_detail(request, id):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['menu_products'] = get_menu_products()
    ctx['page_name'] = 'My inquiry'
    if request.method == 'GET':
        try:
            inquiry = Inquiry.objects.get(id=id)
        except Exception as err:
            logger.error('Can not find order %s' % (id))
            raise Http404

        ctx['inquiry'] = inquiry
        return TemplateResponse(request, System_Config.get_template_name() + '/inquiry_view.html', ctx)
