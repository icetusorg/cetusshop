#coding=utf-8
from django.shortcuts import render
from django.template.loader import render_to_string
from shopcart.models import System_Config,Product,Product_Images,Category,Attribute,ProductPush,ProductPushGroup
from shopcart.utils import my_pagination,get_system_parameters
import json,os
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.http import Http404
from django.http import HttpResponse
from shopcart.functions.product_util_func import get_menu_products
from django.template.response import TemplateResponse
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

def get_page_size():
	try:
		size = int(System_Config.objects.get(name='product_page_size').val)
	except:
		logger.info('"admin_order_list_page_size" is not setted.Use default value 12.')
		size = 12
	return size

# Create your views here.
def detail(request,id):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Product'
	try:
		product = Product.objects.get(id=id)
	except Exception as err:
		logger.error('找不到编号为 %s 的商品。' % [id,])
		raise Http404
	#由于存在外键关系，只需要查出product对象，product所关联的images可以在模板中用product.images.all获得。
	ctx['product'] = product
	ctx['page_key_words'] = product.keywords
	ctx['page_description'] = product.short_desc
	if product.page_title:
		ctx['page_name'] = product.page_title
	else:
		ctx['page_name'] = product.name
	
	'''价格规则改成判断数量了，这段暂时不要
	price_min = product.price
	price_max = product.price
	for attribut in product.attributes.all():
		if attribut.price_adjusment > 0:
			if attribut.price_adjusment + product.price > price_max:
				price_max = attribut.price_adjusment + product.price
		else:
			if product.price + attribut.price_adjusment < price_min:
				price_min = product.price + attribut.price_adjusment
	ctx['price_min'] = price_min
	ctx['price_max'] = price_max
	
	
	
	if product.get_max_price_max - price_min < 0.01:
		ctx['has_price_range'] = False
	else:
		ctx['has_price_range'] = True
	'''
		
	if request.method =='GET': #正常访问，返回动态页面
		#检查商品是否已经加入了用户的愿望清单
		if request.user.is_authenticated():
			wish_list = request.user.wishs.all()
			for wish in wish_list:
				if product == wish.product:
					logger.debug('The product which id is %s has been added to user\'s wishlist.' % (product.id))
					ctx['is_my_wish'] = True
		
		#获取特定的模板，先判断商品是否设置了模板，没有则判断商品所在的分类是否设置了指定模板，都没有，则使用系统统一模板
		template = '/product_detail.html'
		
		if product.categorys.count() > 0:
			cat = product.categorys.all()[0]
			if cat.detail_template != '':
				template = '/custmize/product/' + cat.detail_template
		
		if product.detail_template != '':
			if product.detail_template.upper() == 'USE_DEFAULT':
				#强行指定用默认模板
				template = '/product_detail.html'
			else:
				template = '/custmize/product/' + product.detail_template
		
		return TemplateResponse(request,System_Config.get_template_name() + template, ctx)
	elif request.method == 'POST':#通过ajax访问，生成静态文件
		content = render_to_string(System_Config.get_template_name() + '/product_detail.html', ctx)
		result_dict = {}
		try:
			import codecs,os
			#先获取商品所属分类，作为目录
			category_list = product.categorys.all()
			f = None
			dir = ''
			for cat in category_list:
				dir = 'www/' + cat.get_dirs()
				dir_http = cat.get_dirs()
				if not os.path.exists(dir):
					os.makedirs(dir)
				f = codecs.open(dir + product.static_file_name ,'w','utf-8')
				f.write(content)
				f.close()
			result_dict['success'] = True
			result_dict['message'] = _('File already generated.')
			result_dict['static_url'] = dir_http + product.static_file_name
		except Exception as err:
			logger.error('写文件失败。' + str(err))
			result_dict['success'] = False
			result_dict['message'] = _('File generate failed.')
		finally:
			if f is not None:
				f.close()
		return JsonResponse(result_dict)
		
def category(request,category_id):
	return view_list(request,category_id = category_id)

		
def view_list(request,category_id=None):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Product'
	
	template = '/product_list.html'
	
	if request.method =='GET':
		product_list = None
		if 'sort_by' in request.GET:
			if 'direction' in request.GET:
				if 'desc' == request.GET['direction']:
					product_list = Product.objects.filter(is_publish=True).order_by(request.GET['sort_by']).reverse()
				else:
					product_list = Product.objects.filter(is_publish=True).order_by(request.GET['sort_by'])
				
				ctx['direction'] = request.GET['direction']
			else:
				product_list = Product.objects.filter(is_publish=True).order_by(request.GET['sort_by'])
		else:
			logger.debug("all products")
			product_list = Product.objects.filter(is_publish=True).order_by('update_time').reverse()
			logger.debug('Products count in product_list : [%s]' % len(product_list))
		
		#按分类筛选
		logger.debug('category_id : %s ' % category_id)
		if category_id:
			#查找该分类是否设置了自定义的分类模板
			try:
				category = Category.objects.get(id=category_id)
				from .category import get_all_children
				cat_list = get_all_children(category,[])
				logger.debug('cat_list: %s' % cat_list)
				ctx['page_key_words'] = category.keywords
				ctx['page_description'] = category.short_desc
				if category.page_title:
					ctx['page_name'] = category.page_title
				else:
					ctx['page_name'] = category.name
				if category.category_template:
					template = '/custmize/category/' + category.category_template
				product_list = product_list.filter(categorys__in = cat_list)
				product_list = list(set(product_list))
				product_list = sorted(product_list,key= lambda product:product.update_time,reverse=True)
				logger.debug('Products count in product_list : [%s]' % len(product_list))
			except Exception as err:
				logger.error('Can not find category which id is %s. Error message is %s ' % (category_id,err))
				
			#设置分类专用的标题和描述
			ctx['category_title'] = category.name
			ctx['category_desc'] = category.description
			
		logger.debug("no sort_by")
		if 'page_size' in request.GET:
			page_size = request.GET['page_size']
		else:
			try:
				page_size = int(System_Config.objects.get(name='product_page_size').val)
			except:
				page_size = 12
		
		product_list, page_range = my_pagination(request=request, queryset=product_list,display_amount=page_size)
		
		ctx['product_list'] = product_list
		ctx['page_range'] = page_range
		return TemplateResponse(request,System_Config.get_template_name() + template,ctx)


def query_product_show(request):
	ctx = {}
	ctx['system_para'] = get_system_parameters()
	ctx['menu_products'] = get_menu_products()
	ctx['page_name'] = 'Product'
	
	if request.method =='GET':
		query_condition = request.GET.get('query','')
		logger.debug('Query_String is %s ' % query_condition)
		from django.db.models import Q
		product_list = Product.objects.filter(Q(name__icontains=query_condition))
		#icontains是大小写不敏感的，contains是大小写敏感的
		
		
		if 'page_size' in request.GET:
			page_size = request.GET['page_size']
		else:
			page_size = get_page_size()
		product_list, page_range = my_pagination(request=request, queryset=product_list,display_amount=page_size)
		
		ctx['product_list'] = product_list
		ctx['page_range'] = page_range
		return TemplateResponse(request,System_Config.get_template_name() + '/product_list.html',ctx)
		
		
def ajax_get_product_info(request):
	logger.info('Entered the ajax_get_product_info function')
	product_to_get = json.loads((request.body).decode())

	logger.debug('product_id:%s' % [product_to_get['product_id']])
	product = Product.objects.get(id=product_to_get['product_id'])

	result_dict = {}
	result_dict['success'] = False
	result_dict['message'] = ''

	logger.debug('the attr_list length:%s' % [len(product_to_get['attr_list'])])
	logger.debug('the product.attributes length:%s' % [len(product.attributes.all())])
	
	#商品是否有额外属性
	if not product.attributes.all():
		#没有额外属性
		logger.info('Product has no extra attributes.')
		result_dict['success'] = False
		result_dict['message'] = null
		return result_dict	

	#attr是否已经全了
	pa = product.attributes.all()[0]
	attr_type_count = len(pa.attribute.all())
	logger.debug('Product has %s kinds attributes.' % [attr_type_count])

	
	para_list = product_to_get['attr_list']
	para_list = [int(attr) for attr in para_list]#转换成数值型
	para_list.sort() #排序
	#logger.debug('>>>>para_list:' + str(para_list))
	
	#attr_avaliable_set = set([])
	for pa in product.attributes.all():
		attr_id_list = [attr.id for attr in pa.attribute.all()]
		#logger.debug('>>>>attr_id_list:' + str(attr_id_list))
		if set(para_list) <= set(attr_id_list):#判断para_list是否是attr_id_list的子集
			temp = set(attr_id_list) - set(para_list) #求差集
			if len(temp) == 0:
				#没有差集，已经选择全面了
				result_dict['success'] = True
				product_extra = {}
				product_extra['price'] = product.price + pa.price_adjusment
				product_extra['quantity'] = pa.quantity
				product_extra['sub_item_number'] = pa.sub_item_number
				product_extra['pa_id'] = pa.id
				#20160523，添加最小购买量
				
				#product_extra['min_order_quantity'] = pa.min_order_quantity
				#最小下单量控制到商品层
				product_extra['min_order_quantity'] = product.min_order_quantity
				
				if pa.image:
					product_extra['image_url'] = pa.image.image
					product_extra['show_image'] = True
				else:
					product_extra['show_image'] = False
					product_extra['image_url'] = ''
				result_dict['message'] = product_extra
				result_dict['success'] = True
				#return JsonResponse(result_dict)
			#else:
			#	attr_avaliable_set = attr_avaliable_set | temp #求并集
	#进入到这里，说明前面没有选择全
	#result_dict['success'] = False
	
	#组建可以选择的列表和不可选择的列表
	'''
	算法：
		假设有3个组
		1组： A B
		2组： C D
		3组： E F
		理论上可以有 ACE/ACF/ADE/ADF/BCE/BCF/BDE/BDF 这样8种组合
		事实上，实际商品可能并没有8种组合，也许只有 ACE/ACF 和 BDE/BDF 这么4种组合，甚至只有 ACE  和  BDE/BDF 这么三种组合
		需要在前台利用灰色的框来表示当前的组合选择下，还有哪些可以选，就需要找出哪些按钮应该亮起。
		算法可以举例表述为：
		例如 当前选择了AE：
		第一步：先找出PA中带有A和E的所有组合，比如找到了 ACE/ACF 和 BDE
		第二步：找出既有A又有E的组合，找到了ACE。所以C亮起。
		第三步：逐个分析与A或者E同组的选项，比如B，查找是否存在 BE的组合，存在则亮起，不存在则灰掉；同样，也要逐个分析与E同组的选项，比如F，不存在AF组合的话，就要将F灰掉。
		经过上面的筛选，应该可以找到当前组合条件下，可以点选的选项了。
	'''
	available_set = check_available_attributes(para_list,product)
	available_ret = []
	for attr in available_set:
		tmp = '%s|%s' % (attr.id,attr.group.group_type)
		available_ret.append(tmp)
	result_dict['available_set'] = available_ret

	return JsonResponse(result_dict)
	
def check_available_attributes(para_list,product):
	available_list = set()

	attribute_list = Attribute.objects.filter(id__in=para_list)
	
	
	logger.debug('attribute_list:%s' % attribute_list)
	pa_list = product.attributes.all()
	#logger.debug('pa_list:%s' % pa_list)
	
	#1 先找出PA中，带有attribute_list的中每一个属性的所有组合
	pa_with_selected_list = pa_list.filter(attribute__in = attribute_list)
	#logger.debug('pa_with_selected_list:%s' % pa_with_selected_list)
	
	#2 在上一步的结果中找出含有所有组合的选项
	pa_with_selected_combined_list = pa_with_selected_list
	for attr in attribute_list:
		pa_with_selected_combined_list = pa_with_selected_combined_list.filter(attribute=attr)
	pa_with_selected_combined_list = list(set(pa_with_selected_combined_list))
	#logger.debug('pa_with_selected_combined_list:%s' % pa_with_selected_combined_list)
	
	#3 将pa_with_selected_combined_list中还没有选择的选项加入到available_list中
	tmp_attr_list = set()
	for pa in pa_with_selected_combined_list:
		for attr in pa.attribute.all():
			tmp_attr_list.add(attr)
	#logger.debug('tmp_attr_list:%s' % tmp_attr_list)
	for attr in tmp_attr_list:
		available_list.add(attr)
	#logger.debug('available_list:%s' % available_list)
	
	#4 将attribute_list的元素拿出来，逐个分析其同族的元素，是否在pa中存在相应的组合，存在则加入available_list
	for attr in attribute_list:
		#找出同族元素
		group_members_set = set(attr.group.attributes.all())
		group_members_set.remove(attr)
		logger.debug('the members in attr %s group is: %s' %(attr,group_members_set))
		#逐个查找是否存在 group_members_set中元素与attribute_list其它元素组合的pa
		attribute_set = set(attribute_list)
		attribute_set.remove(attr)
		for attr in group_members_set:
			tmp = pa_list.filter(attribute=attr)
			for attr_other in attribute_set:
				tmp = tmp.filter(attribute=attr_other)
			if tmp.count() > 0:
				available_list.add(attr)
			logger.debug('当前同族的元素是：%s , 筛选后的组合为：%s .' % (attr,tmp))
		
	logger.debug('available_list:%s' % available_list)	
	return available_list
	
	
	
	
def ajax_get_product_images(request,method='main'):
	if request.is_ajax():
		result = {}
		result['success'] = False
		id = request.POST.get('id')
		try:
			product = Product.objects.get(id=id)
		except Exception as err:
			logger.error('Can not find product [%s].\n Error Message:%s' % (id,err))
			result['message'] = 'Can not find product.'
			return JsonResponse(result)
			
		if method == 'main':
			img_list = product.get_main_image_list()
		else:
			img_list = product.get_all_image_list()
		
		data = []
		for img in img_list:
			image = {}
			image['image'] = img.image
			image['thumb'] = img.thumb
			image['id'] = img.id
			image['alt'] = img.alt_value
			image['product_id'] = product.id
			data.append(image)
		
		result['success'] = True
		result['image_list'] = data
		return JsonResponse(result)
	else:
		raise Http404
		

def ajax_get_product_description(request,id):
	logger.info('Entered the ajax_get_product_description function')
	product_desc = ''
	if request.is_ajax():
		try:
			product = Product.objects.get(id=id)
			product_desc = product.description
		except Exception as err:
			logger.error('检索id为%s的商品不存在.' % [id])
	return HttpResponse(product_desc)
	
def get_push_product(request):
	type = request.GET.get('type','')
	result_dict = {}
	try:
		group = ProductPushGroup.objects.get(code=type)
	except Exception as err:
		logger.info('Can not find product push group %s' % type)
		products = []
		return JsonResponse(result_dict)
	
	product_list = ProductPush.objects.filter(group=group).order_by('-sort_order')
	products = []
	for p in product_list:
		products.append(p.serialization())
	
	result_dict['success'] = True
	result_dict['products'] = products
	return JsonResponse(result_dict)

