# coding=utf-8
from django.shortcuts import render, redirect
from shopcart.models import Article, System_Config, Album, ArticleBusiCategory
from shopcart.forms import article_basic_info_form, article_detail_info_form
from shopcart.utils import my_pagination, get_serial_number, get_system_parameters
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.template.response import TemplateResponse
import logging

logger = logging.getLogger('icetus.shopcart')


def get_page_size():
    try:
        size = System_Config.objects.get(name='admin_article_list_page_size').val
    except:
        logger.info('"admin_order_list_page_size" is not setted.Use default value 8.')
        size = 8
    return size


@staff_member_required
@transaction.atomic()
def set_image(request):
    ctx = {}
    ctx['page_name'] = '文章图片管理'

    if request.method == 'POST':
        result = {}
        result['success'] = False
        result['message'] = '文章图片信息保存失败'

        method = request.POST.get('method', '')
        if method == 'set_main':
            try:
                article_id = request.POST.get('article_id', '')
                picture_id = request.POST.get('picture_id', '')
                article = Article.objects.get(id=article_id)
                picture = Album.objects.get(id=picture_id)
            except Exception as err:
                logger.info(
                    'Can not find article [%s] or picture [%s]. \n Error Message: %s' % (article_id, picture_id, err))

            article.image = picture.image
            article.save()
            Album.objects.filter(item_id=article_id).update(sort=0)  # 先把所有图的sort设为0

            Album.objects.filter(id=picture_id).update(sort=-1)  # 需要设为首图的Sort设为1



            result['success'] = True
            result['message'] = '文章图片信息保存成功'
            return JsonResponse(result)
        elif method == 'delete':
            picture_id = request.POST.get('picture_id', '')
            picture = None

            try:
                picture = Album.objects.get(id=picture_id)
            except Exception as err:
                logger.info('Can not find  picture [%s] in Product_Images. \n Error Message: %s' % (picture_id, err))

            if picture:
                picture.remove_file()
                picture.delete()
                result['success'] = True
                result['message'] = '文章图片信息删除成功'
            else:
                result['message'] = '文章图片信息删除失败，可能图片已经被删除了。'

            return JsonResponse(result)
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def article_make_static(request):
    ctx = {}
    ctx['article_list'] = Article.objects.all()
    return TemplateResponse(request, 'admin/article/make_static.html', ctx)


@staff_member_required
@transaction.atomic()
def delete(request):
    result_dict = {}
    result_dict['success'] = False
    result_dict['message'] = '表单填写的内容不合法，请检查。'
    if request.method == 'POST':
        logger.info('进入删除')
        article_id_list = request.POST.getlist('is_oper', [])
        logger.info('id %s' % article_id_list)
        count = 0
        if article_id_list:
            for id in article_id_list:
                article = Article.objects.get(id=id)
                article.remove_file()
                article.delete()
                count += 1
            result_dict['success'] = True
            result_dict['message'] = '%s 篇文章被成功删除' % count
        else:
            result_dict['message'] = '没有选择任何文章进行操作。'
    return JsonResponse(result_dict)


@staff_member_required
@transaction.atomic()
def sort(request):
    result_dict = {}
    result_dict['success'] = False
    result_dict['message'] = '表单填写的内容不合法，请检查。'
    if request.method == 'POST':
        article_id_list = request.POST.getlist('is_oper', [])
        count = 0
        if article_id_list:
            for id in article_id_list:
                article = Article.objects.get(id=id)
                article.sort_order = request.POST.get('sort_%s' % id, '0')
                article.save()

                count += 1
            result_dict['success'] = True
            result_dict['message'] = '%s 篇文章的排序被重新设置' % count
        else:
            result_dict['message'] = '没有选择任何文章进行操作。'
    return JsonResponse(result_dict)


@staff_member_required
@transaction.atomic()
def detail(request, id):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = '文章管理'

    if request.method == 'GET':
        try:
            article = Article.objects.get(id=id)
            ctx['article'] = article
            ctx['method'] = article.category
            return TemplateResponse(request, System_Config.get_template_name('admin') + '/article_detail.html', ctx)
        except Exception as err:
            logger.error("Can not find artice which id is %s . \n Error message: %s" % (id, err))
            raise Http404
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def article_basic_edit(request):
    ctx = {}

    result = {}
    result['success'] = False
    result['message'] = ''
    result['data'] = {}

    # 加载自定义模板供选择
    from .file import file_list
    template_list = file_list(System_Config.get_template_name('client') + '/custmize/', 'custmize_template_article')
    logger.debug('custome_templates: %s' % template_list)
    ctx['custmize_template'] = template_list

    if request.method == 'GET':
        id = request.GET.get('id', '')
        method = request.GET.get('method', 'blog')
        if id != '':
            try:
                article = Article.objects.get(id=id)
                ctx['article'] = article

                # 图片处理URL
                ctx['upload_url'] = '/admin/file-upload/article/%s/' % id
                logger.debug('upload_url:%s' % ctx['upload_url'])

                ctx['file_delete_url'] = '/file-delete/article'

                try:
                    ctx['image_list'] = Album.objects.filter(item_type='article').filter(item_id=id).order_by(
                        'create_time').reverse()
                    logger.debug("ctx['image_list']:%s" % ctx['image_list'])
                except Exception as err:
                    logger.error("Error:%s" % err)
                    ctx['image_list'] = []

                logger.debug('article category:%s' % article.category)

                if article.category == Article.ARTICLE_CATEGORY_BLOG:
                    ctx['is_blog'] = True
                else:
                    ctx['is_blog'] = False

            except Exception as err:
                logger.error('Can not find article which id is %s. The error message is %s' % (id, err))
                if method == 'blog':
                    ctx['is_blog'] = True
                else:
                    ctx['is_blog'] = False
        else:
            if method == 'blog':
                ctx['is_blog'] = True
            else:
                ctx['is_blog'] = False

        # 放入文章的业务分类
        from .article_busi_category import get_all_category

        ctx['category_list'] = get_all_category()
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/article_detail.html', ctx)
    elif request.method == 'POST':
        try:
            article = Article.objects.get(id=request.POST['id'])
            form = article_basic_info_form(request.POST, instance=article)
        except:
            article = None
            form = article_basic_info_form(request.POST)
            logger.info('New article to store.')

        if form.is_valid():
            article = form.save()

            # # 只有属于博客类的文章才需要保存分类
            # if article.category == Article.ARTICLE_CATEGORY_BLOG:
            #     category_id = request.POST.get('busi_category', '')
            #     if category_id:
            #         try:
            #             category = ArticleBusiCategory.objects.get(id=category_id)
            #         except Exception as err:
            #             logger.error('Can not find article_busi_category [%s].\nError Message:%s' % (category_id, err))
            #             result['success'] = False
            #             result['message'] = '文章保存失败，请选择文章分类。'
            #             result['data'] = {}
            #             return JsonResponse(result)
            #         article.busi_category = category
            #         article.save()

            result['success'] = True
            result['message'] = '文章保存成功'
            data = {}
            data['article_id'] = article.id
            result['data'] = data
        else:
            result['success'] = False
            result['message'] = '文章保存失败'
            result['data'] = {}

        return JsonResponse(result)
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def article_detail_info_manage(request):
    result = {}
    result['success'] = False
    result['message'] = ''
    if request.method == 'POST':
        try:
            article = Article.objects.get(id=request.POST['id'])
            form = article_detail_info_form(request.POST, instance=article)
        except Exception as err:
            logger.error('Error: %s' % err)
            raise Http404

        if form.is_valid():
            # 判断自定义文件名是否重复
            url = form.cleaned_data['static_file_name']
            if url:
                try:
                    a = Article.objects.get(static_file_name=url)
                except Exception as err:
                    a = None

                if a and a != article:
                    # 能找到，说明重名了
                    result['success'] = False
                    result['message'] = '自定义URL与%s商品重复！' % a.title
                    return JsonResponse(result)
            article = form.save()
            # 只有属于博客类的文章才需要保存分类
            if article.category == Article.ARTICLE_CATEGORY_BLOG:
                category_id = request.POST.get('busi_category', '')
                if category_id:
                    try:
                        category = ArticleBusiCategory.objects.get(id=category_id)
                    except Exception as err:
                        logger.error('Can not find article_busi_category [%s].\nError Message:%s' % (category_id, err))
                        result['success'] = False
                        result['message'] = '文章保存失败，请选择文章分类。'
                        result['data'] = {}
                        return JsonResponse(result)
                    article.busi_category = category
                    article.save()
            logger.debug('article:%s' % article.short_desc)
            result['success'] = True
            result['message'] = '文章详细信息保存成功'
        else:
            result['message'] = '文章详细信息保存失败'
        return JsonResponse(result)
    elif request.method == 'GET':
        raise Http404
    else:
        raise Http404


@staff_member_required
@transaction.atomic()
def article_picture_manage(request):
    result_dict = {}
    result_dict['success'] = False
    result_dict['message'] = ''

    if request.method == 'POST':
        # 先找出文章
        try:
            article = Article.objects.get(id=request.POST.get('id'))
        except Exception as err:
            logger.error('Can not find article which id is %s.' % id)
            result_dict['message'] = '文章找不到，可能商品已经被删除了，请重试。'
            return JsonResponse(result_dict)

        # 保存主图和缩略图
        image_url = request.POST.get('article_image')
        article.image = image_url
        dot_index = image_url.rfind('.')
        thumb_url = image_url[:dot_index] + "-thumb" + image_url[dot_index:]
        logger.debug("thumb_url:%s" % thumb_url)
        article.thumb = thumb_url
        article.save()

        result_dict['success'] = True
        result_dict['message'] = '图片设置成功'

    return JsonResponse(result_dict)


@staff_member_required
@transaction.atomic()
def list_view(request):
    ctx = {}
    ctx['system_para'] = get_system_parameters()
    ctx['page_name'] = '文章管理'

    if request.method == 'GET':

        type = request.GET.get('type', '')
        ctx['type'] = type
        # 默认只查询博客文章
        if not type:
            type = '0'

        query_item = request.GET.get('query_item', '')
        ctx['query_item'] = query_item
        logger.debug('query item : %s' % query_item)

        item_value = request.GET.get('item_value', '')
        ctx['item_value'] = item_value
        logger.debug('item_value : %s' % item_value)
        query_busi_category = request.GET.get('query_busi_category', '')
        ctx['query_busi_category_id'] = query_busi_category
        try:
            busi_cat = ArticleBusiCategory.objects.get(id=query_busi_category)
            ctx['query_busi_category_name'] = busi_cat.name
        except:
            ctx['query_busi_category_name'] = ''

        logger.debug('query_busi_category : %s' % query_busi_category)

        # all = Article.objects.all().order_by('-update_time')
        all = Article.objects.all().order_by('-sort_order')
        if type:
            all = all.filter(category=type)

        if query_item == 'title':
            if item_value:
                from django.db.models import Q
                all = all.filter(Q(title__icontains=item_value))

        if query_busi_category:
            all = all.filter(busi_category=query_busi_category)

        page_size = get_page_size()

        count = len(all)
        artile_list, page_range, current_page = my_pagination(request=request, queryset=all, display_amount=page_size)
        logger.debug('current_page:%s' % current_page)

        # 为页面准备分类的下拉列表
        from shopcart.myadmin.article_busi_category import get_all_category
        busi_category_list = get_all_category()
        logger.debug('busi_category_list : %s' % busi_category_list)
        ctx['busi_category_list'] = busi_category_list

        ctx['article_list'] = artile_list
        ctx['page_range'] = page_range
        ctx['page_size'] = page_size
        ctx['current_page'] = current_page
        ctx['article_count'] = count
        return TemplateResponse(request, System_Config.get_template_name('admin') + '/article_list.html', ctx)
    else:
        raise Http404
