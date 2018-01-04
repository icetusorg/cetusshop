# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from shopcart.models import System_Config, CustomizeURL, ClientMenu, Slider,Menu
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse
from shopcart.utils import get_system_parameters, customize_tdk
import json
from django.utils.translation import ugettext as _
from shopcart.functions.product_util_func import get_menu_products
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
import time
import logging

logger = logging.getLogger('icetus.shopcart')


# Create your views here.
def view_index(request, tdk=None):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['menu_products'] = get_menu_products()

    def get_all_top_menu():
        top_menu_list = Menu.objects.filter(parent=None)
        return top_menu_list

    top_menu_list = get_all_top_menu()
    ctx['menu_list'] = top_menu_list
    if not tdk:
        try:
            cust = CustomizeURL.objects.get(name='首页')
            if cust.is_customize_tdk:
                tdk = {}
                tdk['page_title'] = cust.page_name
                tdk['keywords'] = cust.keywords
                tdk['short_desc'] = cust.short_desc
        except Exception as err:
            tdk = None

    if tdk:
        customize_tdk(ctx, tdk)

    # from .oauth import SocialSites, SocialAPIError
    # socialsites = SocialSites()

    # s = socialsites.get_site_object_by_name('facebook')
    # ctx['oauth'] = s.authorize_url

    # 判断网站服务是否到期

    maturity_data = System_Config.objects.get(name='maturity_data').val  # 获取到期时间
    new_maturity_data = time.strptime(maturity_data, "%Y-%m-%d %H:%M:%S")  # 转化为时间戳
    new_maturity_data_time = time.mktime(new_maturity_data)

    now_time = int(time.time())  # 获取当前时间

    if now_time - new_maturity_data_time >= 0:
        return TemplateResponse(request, System_Config.get_template_name() + '/index_error.html', ctx)
    else:
        return TemplateResponse(request, System_Config.get_template_name() + '/index.html', ctx)


# 刷新验证码
def refresh_captcha(request):
    to_json_response = dict()
    to_json_response['status'] = 1
    to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
    to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
    return HttpResponse(json.dumps(to_json_response), content_type='application/json')


def get_menu(request):
    code = request.GET.get('menu_name', 'common_header')
    try:
        menu = ClientMenu.objects.get(code=code)
    except Exception as err:
        logger.error('Can not find menu %s. \n Error Message:%s' % (code, err))
        menu = ''

    result_dict = {}
    result_dict['success'] = True
    result_dict['data_menu'] = menu.content
    return JsonResponse(result_dict)


def get_slider_images(request):
    code = request.GET.get('slider_name', '')
    try:
        slider = Slider.objects.get(code=code)
    except Exception as err:
        logger.error('Can not find slider %s. \n Error Message:%s' % (code, err))
        slider = None

    result_dict = {}
    result_dict['success'] = True
    image_list = []
    for img in slider.get_image_list():
        image = {}
        image['image'] = img.image
        image['href'] = img.href
        image['alt'] = img.alt_value
        image_list.append(image)
    result_dict['image_list'] = image_list
    return JsonResponse(result_dict)
