# coding=utf-8
from django.conf import settings
from django.http import HttpResponseRedirect
import sys
from django.views.debug import technical_500_response
import logging
from django.http import HttpResponse, JsonResponse
from shopcart.models import Visitor
from . import models
import time
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, Http404

logger = logging.getLogger('icetus.shopcart')


# 获取客户端ip
def get_remote_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
        logger.debug('There is HTTP_X_FORWARDED_FOR in request.META,ip is:%s' % ip)
    else:
        ip = request.META['REMOTE_ADDR']
        logger.debug('Get ip from REMOTE_ADDR is:%s' % ip)
    return ip


class MyLoginCheckMiddleware:
    def process_request(self, request):
        # logger.debug('Come into the process_request.')
        myuser = request.user
        if myuser.is_anonymous():
            # 匿名用户，不控制
            # path = request.path
            pass
        else:
            # logger.debug('%s' % myuser)
            path = request.path_info.lstrip('/')
            # logger.debug('path:%s' % path)
            if not path == 'user/login/':
                if myuser.is_active == False:
                    # logger.info('%s user has been banned. Reject!' % request.user.email)
                    from django.contrib import auth
                    auth.logout(request)
                    return HttpResponseRedirect(settings.LOGIN_URL)

    def process_template_response(self, request, response):
        logger.debug('Come into the process_template_response')
        logger.debug('Add custmizeVar into context_data...')
        from shopcart.models import CustomizeVar
        vars = {}
        for var in CustomizeVar.objects.all():
            vars[var.name] = var.value

        vars['full_path'] = request.get_full_path()
        vars['path'] = request.path
        response.context_data['customize_var'] = vars
        # logger.debug('customize_var:%s' % vars)


        from shopcart.utils import get_system_parameters
        response.context_data['system_para'] = get_system_parameters()

        # logger.debug("Look up: %s" % response.context_data['customize_var'])
        return response

    # 对超级用户，可以看到报错信息
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())

            # 访问统计


class vistor:
    def process_request(self, request):
        # logger.debug('进入访问数据统计')
        ip = get_remote_ip(request)

        # try:
        if models.Visitor.objects.filter(ip_address=ip,
                                         create_time__gte=(datetime.utcnow() - timedelta(hours=1))):
            return None
        else:
            models.Visitor.objects.create(ip_address=ip)
            # logger.debug('数据库写入成功')
        return None
