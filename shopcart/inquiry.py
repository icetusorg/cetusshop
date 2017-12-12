# coding=utf-8
from django.shortcuts import render, redirect, render_to_response
from shopcart.models import System_Config
from shopcart.utils import get_system_parameters
from django.core.context_processors import csrf
from shopcart.forms import inquiry_form
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext as _
from django.db import transaction
from django.http import Http404
from shopcart import signals
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')


@transaction.atomic()
def add(request):
    ctx = {}
    ctx.update(csrf(request))
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = 'Inquiry'

    result_dict = {}

    if request.method == 'POST':
        form = inquiry_form(request.POST)  # 获取Post表单数据

        logger.info('验证码验证')
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
