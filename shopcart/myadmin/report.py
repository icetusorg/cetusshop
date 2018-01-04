# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from shopcart.models import System_Config, Order, Visitor, Inquiry
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
import logging

logger = logging.getLogger('icetus.shopcart')


@staff_member_required
def order_report(request):
    result = {}
    if request.method == "POST":
        method = request.POST.get('method', '')
        if method == "week_count":
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')

            from shopcart.functions import date_time_util
            logger.debug('today:%s' % date_time_util.datetime())

            date_list = []
            for i in range(6):
                date_list.append(date_time_util.get_today_only_month(-i))

            date_list.reverse()
            logger.debug('date_list:%s' % date_list)

            index_list = []

            length = len(date_list)
            for i, date in enumerate(date_list):
                if i < length:
                    logger.debug('当前第%s次，Date:%s' % (i, date))
                    visitor = Visitor.objects.filter(create_time__startswith=date_list[i]).count()
                    inquiry = Inquiry.objects.filter(create_time__startswith=date_list[i]).count()

                    index = {}
                    index['order'] = i
                    index['date'] = date
                    index['count'] = visitor
                    index['amount'] = inquiry
                    index_list.append(index)

            result['data'] = index_list
            result['success'] = True
            return JsonResponse(result)
        elif method == "summary":
            order_list = []

            control_id_list = ['count_for_pay', 'count_for_ship', 'count_for_close', 'count_for_finish',
                               'count_for_error']

            from django.db.models import Q

            order = {}
            order['control_id'] = 'count_for_pay'
            order['count'] = Order.objects.filter(
                Q(status=Order.ORDER_STATUS_PLACE_ORDER) | Q(status=Order.ORDER_STATUS_PAYED_UNCONFIRMED)).count()
            order_list.append(order)

            order = {}
            order['control_id'] = 'count_for_ship'
            order['count'] = Order.objects.filter(
                Q(status=Order.ORDER_STATUS_PAYED_SUCCESS) | Q(status=Order.ORDER_STATUS_COLLECT_SUCCESS)).count()
            order_list.append(order)

            order = {}
            order['control_id'] = 'count_for_close'
            order['count'] = Order.objects.filter(Q(status=Order.ORDER_STATUS_CLOSED)).count()
            order_list.append(order)

            order = {}
            order['control_id'] = 'count_for_finish'
            order['count'] = Order.objects.filter(Q(status=Order.ORDER_STATUS_COMPLETE)).count()
            order_list.append(order)

            order = {}
            order['control_id'] = 'count_for_error'
            order['count'] = Order.objects.filter(Q(status=Order.ORDER_STATUS_ERROR)).count()
            order_list.append(order)

            result['data'] = order_list
            result['success'] = True
            return JsonResponse(result)
        else:
            raise Http404
    else:
        raise Http404
