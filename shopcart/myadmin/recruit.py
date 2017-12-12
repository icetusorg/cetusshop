# coding=utf-8
from django.shortcuts import render, redirect
from shopcart.models import Article, System_Config, Album, ArticleBusiCategory, Recruit
from shopcart.forms import recruit_basic_info_form
from shopcart.utils import my_pagination, get_serial_number, get_system_parameters
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.template.response import TemplateResponse
import logging

logger = logging.getLogger('icetus.shopcart')


def get_page_size():
    size = 8
    return size


# @staff_member_required
# @transaction.atomic()
# def article_make_static(request):
#     ctx = {}
#     ctx['article_list'] = Article.objects.all()
#     return TemplateResponse(request, 'admin/article/make_static.html', ctx)


@staff_member_required
@transaction.atomic()
def delete(request):
    result_dict = {}
    result_dict['success'] = False
    result_dict['message'] = '表单填写的内容不合法，请检查。'
    if request.method == 'POST':
        article_id_list = request.POST.getlist('is_oper', [])
        logger.debug(article_id_list)

        count = 0
        if article_id_list:
            for id in article_id_list:
                recruit = Recruit.objects.get(id=id)
                recruit.delete()
                count += 1
            result_dict['success'] = True
            result_dict['message'] = '%s 篇招聘文章被成功删除' % count
        else:
            result_dict['message'] = '没有选择任何招聘文章进行操作。'
    return JsonResponse(result_dict)


@staff_member_required
@transaction.atomic()
def sort(request):
    result_dict = {}
    result_dict['success'] = False
    result_dict['message'] = '表单填写的内容不合法，请检查。'
    if request.method == 'POST':
        article_id_list = request.POST.getlist('is_oper', [])
        logger.debug('article_id_list:%s' % article_id_list)
        count = 0
        if article_id_list:
            for id in article_id_list:
                recruit = Recruit.objects.get(id=id)
                recruit.sort_order = request.POST.get('sort_%s' % id, '0')
                recruit.save()
                count += 1
            result_dict['success'] = True
            result_dict['message'] = '%s 篇文章的排序被重新设置' % count
        else:
            result_dict['message'] = '没有选择任何文章进行操作。'
    return JsonResponse(result_dict)


@staff_member_required
@transaction.atomic()
def recruit_basic_edit(request):
    ctx = {}

    result = {}
    result['success'] = False
    result['message'] = ''
    result['data'] = {}

    if request.method == 'GET':
        ctx = {}

        result = {}
        result['success'] = False
        result['message'] = ''
        result['data'] = {}

        id = request.GET.get('id', '')
        logger.debug('获取ID %s' % id)
        if id != '':
            try:
                recruit = Recruit.objects.get(id=id)
                ctx['recruit'] = recruit
            except Exception as err:
                logger.error('Can not find article which id is %s. The error message is %s' % (id, err))
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/recruit_detail.html', ctx)
    elif request.method == 'POST':

        try:
            recruit = Recruit.objects.get(id=request.POST['id'])
            logger.debug('获取recruit %s' % recruit)
            form = recruit_basic_info_form(request.POST, instance=recruit)
        except:
            recruit = None
            form = recruit_basic_info_form(request.POST)
            logger.info('New recruit to store.')

        if form.is_valid():
            # 判断自定义文件名是否重复
            url = form.cleaned_data['static_file_name']
            if url:
                try:
                    a = Recruit.objects.get(static_file_name=url)
                except Exception as err:
                    a = None

                if a and a != recruit:
                    # 能找到，说明重名了
                    result['success'] = False
                    result['message'] = '自定义URL与%s重复！' % a.title
                    return JsonResponse(result)

            recruit = form.save()

            logger.info('招聘文章保存成功')
            result['success'] = True
            result['message'] = '招聘文章保存成功'
            data = {}
            data['recruit_id'] = recruit.id
            result['data'] = data
        else:
            result['success'] = False
            result['message'] = '招聘文章保存失败'
            result['data'] = {}

        return JsonResponse(result)
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def list_view(request):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = '招聘管理'

    if request.method == 'GET':

        all = Recruit.objects.all().order_by('-sort_order')

        page_size = get_page_size()

        count = len(all)
        recruit_list, page_range, current_page = my_pagination(request=request, queryset=all, display_amount=page_size)
        logger.debug('current_page:%s' % current_page)

        # 为页面准备分类的下拉列表
        # from shopcart.myadmin.article_busi_category import get_all_category
        # busi_category_list = get_all_category()
        # logger.debug('busi_category_list : %s' % busi_category_list)
        # ctx['busi_category_list'] = busi_category_list

        ctx['recruit_list'] = recruit_list
        ctx['page_range'] = page_range
        ctx['page_size'] = page_size
        ctx['current_page'] = current_page
        ctx['recruit_count'] = count
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/recruit_list.html', ctx)
    else:
        raise Http404
