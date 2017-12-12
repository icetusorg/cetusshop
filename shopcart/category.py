# coding=utf-8
from django.shortcuts import render
from django.template.loader import render_to_string
from shopcart.models import System_Config, Category
from shopcart.utils import my_pagination, get_system_parameters
import json, os
from django.http import JsonResponse
from django.http import Http404
from shopcart.functions.product_util_func import get_menu_products
from django.utils.translation import ugettext as _
import logging

logger = logging.getLogger('icetus.shopcart')


def category_list(request, id=None):
    top_category_list = Category.objects.filter(parent=None)

    for cat in top_category_list:
        deal_category(cat)

    logger.debug('id is %s' % id)
    if id:
        cat_selected = Category.objects.get(id=id)
        logger.debug('cat is %s' % cat_selected)

    levle = 0
    top_cat, levle = find_top_category(cat_selected, levle)

    logger.debug('The top cat is %s.\n My levle is %s' % (top_cat, levle))

    ctx = {}
    ctx['categorys'] = top_category_list
    ctx['top_cat'] = top_cat
    ctx['level'] = levle
    logger.debug('Top Categorys : %s' % top_category_list)
    return JsonResponse({'success': 'OK'})


def get_all_categorys():
    category_list = Category.objects.all()
    return category_list


def get_all_top_categorys():
    top_category_list = Category.objects.filter(parent=None)
    return top_category_list


def get_orgnized_category_list(prefix='--'):
    top_list = get_all_top_categorys()
    result_list = []
    tmp = None
    for cat in top_list:
        tmp = {}
        tmp['name'] = cat.name
        tmp['id'] = cat.id
        result_list.append(tmp)
        for cat2 in cat.childrens.all():
            tmp = {}
            tmp['name'] = prefix + cat2.name
            tmp['id'] = cat2.id
            result_list.append(tmp)
            for cat3 in cat2.childrens.all():
                tmp = {}
                tmp['name'] = prefix + prefix + cat3.name
                tmp['id'] = cat3.id
                result_list.append(tmp)
                for cat4 in cat3.childrens.all():
                    tmp = {}
                    tmp['name'] = prefix + prefix + prefix + cat4.name
                    tmp['id'] = cat4.id
                    result_list.append(tmp)
    return result_list


def find_top_category(cat, levle):
    if cat.parent == None:
        return cat, levle
    else:
        levle = levle + 1
        tmp = find_top_category(cat.parent, levle)
        return tmp


def get_all_children(category, cat_list):
    cat_list.append(category)
    for cat in category.childrens.all():
        get_all_children(cat, cat_list)
    return cat_list


def deal_category(category):
    logger.debug('I am %s' % category)
    for cat in category.childrens.all():
        logger.debug('Has children.')
        deal_category(cat)
