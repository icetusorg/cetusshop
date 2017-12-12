# coding=utf-8
from django.db import transaction
from django.utils.translation import ugettext as _
import datetime, uuid
from django.core.serializers import serialize, deserialize
from shopcart.utils import url_with_out_slash

import logging

logger = logging.getLogger('icetus.shopcart')


def get_url(object):
    from shopcart.models import System_Config, Recruit
    url = url_with_out_slash(System_Config.objects.get(name='base_url').val)
    logger.info('进入get_url %s' %url)
    if isinstance(object, Recruit):
        if object.static_file_name == None or object.static_file_name == '':
            return ('%s/recruit/%s' % (url, object.id))
        else:
            return ('%s/%s' % (url, object.static_file_name))
    else:
        return '#'
