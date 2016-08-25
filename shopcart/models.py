#coding=utf-8
from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

import logging
logger = logging.getLogger('icetus.shopcart')

# Create your models here.
class MyUserManager(BaseUserManager):
	def _create_user(self, username, email, password, **extra_fields):
		"""
		Creates and saves a User with the given username, email and password.
		"""
		
		#if not username:
		#    raise ValueError('The given username must be set')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True')

		return self._create_user(username, email, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=254,unique=True, null=True,db_index=True)
	email = models.EmailField('email address', unique=True, db_index=True, max_length=254)
	first_name = models.CharField(max_length=254,null=True)
	middle_name = models.CharField(max_length=254,null=True)
	last_name = models.CharField(max_length=254,null=True)
	mobile_phone = models.CharField(max_length=50,null=True)
	gender = models.CharField(max_length=3,null=True)
	birthday = models.DateField(null=True)
	is_staff = models.BooleanField('staff status', default=False)
	is_active = models.BooleanField('active', default=True)
	create_time = models.DateTimeField(auto_now_add = True,null=True)
	update_time = models.DateTimeField(auto_now = True,null=True)

	USERNAME_FIELD = 'email'

	objects = MyUserManager()

	class Meta:
		db_table = 'myuser'

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return str(self.first_name) + ' ' + str(self.last_name)
		
	def get_human_gender(self):
		if self.gender == '1':
			return 'male'
		elif self.gender == '0':
			return 'female'
		else:
			return 'unknow'


class Address(models.Model):
	useage = models.CharField(max_length=254,default='',null=True)
	is_default = models.BooleanField(default=True)
	first_name = models.CharField(max_length=50,default='',null=True,blank=True)
	last_name = models.CharField(max_length=50,default='',null=True,blank=True)
	user = models.ForeignKey(MyUser,null=True,related_name='addresses')
	country = models.CharField(max_length=50,default='',null=True,blank=True)
	province = models.CharField(max_length=50,default='',null=True,blank=True)
	city = models.CharField(max_length=50,default='',null=True,blank=True)
	district = models.CharField(max_length=50,default='',null=True,blank=True)
	address_line_1 = models.CharField(max_length=100,default='',null=True,blank=True)
	address_line_2 = models.CharField(max_length=100,default='',null=True,blank=True)
	zipcode = models.CharField(max_length=50,default='',null=True,blank=True)
	tel = models.CharField(max_length=50,default='',null=True,blank=True)
	mobile = models.CharField(max_length=50,default='',null=True,blank=True)
	sign_building = models.CharField(max_length=50,default='',null=True,blank=True)
	best_time = models.CharField(max_length=50,default='',null=True,blank=True)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	

@python_2_unicode_compatible
class System_Config(models.Model):
	name = models.CharField(max_length = 100,verbose_name = '参数名称')
	val = models.CharField(max_length = 254,verbose_name = '参数值')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建时间')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新时间')

	@staticmethod
	#获取模板名字
	def get_template_name(type='client'):
		sys_conf = System_Config.objects.get(name='template_name')
		prefix = ''
		if type.lower() == 'client':
			prefix = 'client/'
			return prefix + sys_conf.val
		elif type.lower() == 'admin':
			prefix = 'admin/'
			admin_template = 'default'
			try:
				admin_template = System_Config.objects.get(name='admin_template_name').val
			except Exception as err:
				logger.info('System Parameter "admin_template_name" not defined.Use the default value "default".')
			return prefix + admin_template
		elif type.lower() == 'email':
			prefix = 'email/'
			email_template = 'defalut'
			try:
				email_template = System_Config.objects.get(name='email_template_name').val
			except Exception as err:
				logger.info('System Parameter "email_template_name" not defined.Use the default value "default".')
			return prefix + email_template
		else:
			return sys_conf.val
		
	
	@staticmethod
	#获取网站根路径
	def get_base_url():
		sys_conf = System_Config.objects.get(name='base_url')
		return sys_conf.val
		
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = '系统参数'
		verbose_name_plural = '系统参数'

@python_2_unicode_compatible
class Category(models.Model):
	code = models.CharField(max_length = 100,default='',db_index=True,unique=True,verbose_name = '分类代码')
	name = models.CharField(max_length = 100,default='',verbose_name = '分类名称')
	page_title = models.CharField(max_length = 100,blank=True,default='',verbose_name='网页标题')
	keywords = models.CharField(max_length = 254,default='',blank=True,verbose_name='关键字')
	short_desc = models.CharField(max_length = 254,default='',blank=True,verbose_name='简略描述')
	sort_order = models.CharField(max_length = 100,default='',verbose_name = '排序序号')
	parent = models.ForeignKey('self',null=True,default=None,related_name='childrens',blank=True,verbose_name = '上级分类')
	detail_template = models.CharField(max_length = 254,default='',blank=True,verbose_name='商品详情页指定模板')
	category_template = models.CharField(max_length = 254,default='',blank=True,verbose_name='分类指定模板')
	static_file_name = models.CharField(max_length = 254,db_index=True,unique=True,null=True,blank=True,verbose_name='静态文件名(不包含路径，以html结尾)')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建时间')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新时间')
	
	def get_parent_stack(self):
		from shopcart.utils import Stack  
		s=Stack(20);
		target = self
		while target is not None:
			s.push(target)
			target = target.parent
		return s
		
	def get_dirs(self):
		from shopcart.utils import Stack 
		s = self.get_parent_stack()
		dir = ''
		while not s.isempty():
			dir = dir + s.pop().code + '/'
		return dir

	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = '商品分类'
		verbose_name_plural = '商品分类'

@python_2_unicode_compatible
class Product(models.Model):
	item_number = models.CharField(max_length = 100,default='',db_index=True,blank=True,verbose_name='商品编号')
	name = models.CharField(max_length = 100,default='',verbose_name='商品名称')
	click_count = models.IntegerField(default=0,verbose_name='浏览次数')
	quantity = models.IntegerField(default=0,verbose_name='库存数量')
	warn_quantity = models.IntegerField(default=0,verbose_name='预警库存')
	price = models.FloatField(default=0.0,verbose_name='基准价格')
	market_price = models.FloatField(default=0.0,verbose_name='市场价')
	page_title = models.CharField(max_length = 100,blank=True,default='',verbose_name='网页标题')
	keywords = models.CharField(max_length = 254,default='',blank=True,verbose_name='关键字')
	short_desc = models.CharField(max_length = 254,default='',blank=True,verbose_name='简略描述')
	description = models.TextField(blank=True,verbose_name='详细描述')
	thumb = models.URLField(verbose_name='主缩略图')
	image = models.URLField(verbose_name='主图大图')
	is_free_shipping = models.BooleanField(default=False,verbose_name='是否包邮')
	sort_order = models.IntegerField(default=0,verbose_name='排序序号')
	static_file_name = models.CharField(max_length = 254,null=True,db_index=True,unique=True,blank=True,verbose_name='静态文件名(不包含路径，以html结尾)')
	categorys = models.ManyToManyField(Category,verbose_name='商品分类')
	min_order_quantity = models.IntegerField(default=0,verbose_name='最小下单数量')
	is_publish = models.BooleanField(default=False,verbose_name='上架')
	detail_template = models.CharField(max_length = 254,default='',blank=True,verbose_name='详情页指定模板')
	related_products = models.ManyToManyField('self',null=True,blank=True,related_name='parent_product',verbose_name='关联商品')
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)

	def get_attributes(self):
		pa_list = self.attributes.all()
		attribute_list = Attribute.objects.filter(product_attribute__in=pa_list).distinct()
		attribute_group_list = list(set([attr.group for attr in attribute_list]))#用set去重后，再转回list
		attribute_group_list.sort(key=lambda x:x.position)#利用position字段排序
		
		for ag in attribute_group_list:
			ag.attr_list = [attr for attr in attribute_list if attr.group == ag]
			ag.attr_list.sort(key=lambda x:x.position)
		
		return attribute_group_list
		
	def get_product_detail_images(self):
		return self.images.filter(is_show_in_product_detail=True).order_by('sort')
		
	def get_url(self):
		from shopcart.functions.product_util_func import get_url
		return get_url(self)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '商品'
		verbose_name_plural = '商品'

@python_2_unicode_compatible		
class Product_Images(models.Model):
	#product_id = models.IntegerField(default=0)
	thumb = models.URLField(null=True)
	image = models.URLField(null=True)
	product = models.ForeignKey(Product,default=None,related_name='images',verbose_name='关联的商品')
	is_show_in_product_detail = models.BooleanField(default=False,verbose_name='是否在商品详情中展示')
	sort = models.IntegerField(default=0,verbose_name='排序序号')
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return str(self.id) + ' ' + self.thumb
	
	class Meta:
		verbose_name = '商品相册'
		verbose_name_plural = '商品相册'


@python_2_unicode_compatible
class ParameterGroup(models.Model):
	name = models.CharField(max_length = 100,default='')
	code = models.CharField(max_length = 100,default='') #用于html中用的name属性的
	position = models.IntegerField(default=0)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '参数组合定义'
		verbose_name_plural = '参数组合定义'		
		
@python_2_unicode_compatible
class Parameter(models.Model):
	name = models.CharField(max_length = 100,default='')
	code = models.CharField(max_length = 100,default='') #用于html中用的name属性的
	group = models.ForeignKey(ParameterGroup,null=True,verbose_name='归属的参数组')
	type = models.CharField(max_length = 100,default='',verbose_name='参数类型') #分为text,select两种，一种自己填，一种下拉框选择
	position = models.IntegerField(default=0)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '参数定义'
		verbose_name_plural = '参数定义'
		
@python_2_unicode_compatible
class ParameterValue(models.Model):
	name = models.CharField(max_length = 100,default='',verbose_name='参数值显示名称')
	code = models.CharField(max_length = 100,default='',verbose_name='参数值')
	parameter = models.ForeignKey(Parameter,related_name='values',verbose_name='归属的参数')
	position = models.IntegerField(default=0)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '参数值定义'
		verbose_name_plural = '参数值定义'
		
@python_2_unicode_compatible
class ProductParameter(models.Model):
	product = models.ForeignKey(Product,null=True,related_name='parameters')
	parameter = models.ForeignKey(Parameter,related_name='related_products',verbose_name='参数')
	value_name = models.CharField(max_length=200,null=True,blank=True,verbose_name='参数值')#用于手工填入的值，对应于parameter类型是text类型的
	value = models.ForeignKey(ParameterValue,related_name='related_products',verbose_name='参数值',null=True,blank=True)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.value_name
	
	class Meta:
		verbose_name = '具体的商品参数'
		verbose_name_plural = '具体的商品参数'
	
@python_2_unicode_compatible
class Attribute_Group(models.Model):
	name = models.CharField(max_length = 100,default='')
	group_type = models.CharField(max_length = 100,default='') #分为text,image两种，一种是前台显示文字，一种是前台显示图片
	position = models.IntegerField(default=0)
	code = models.CharField(max_length = 100,default='') #用于html中用的name属性的
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '商品属性组定义'
		verbose_name_plural = '商品属性组定义'

@python_2_unicode_compatible
class Attribute(models.Model):
	group = models.ForeignKey(Attribute_Group,related_name='attributes',null=True)
	name = models.CharField(max_length = 100,default='',verbose_name='外部名称')
	code = models.CharField(max_length = 100,default='',verbose_name='内部代码')
	position = models.IntegerField(default=0)
	thumb = models.URLField(null=True,default=None,blank=True)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.code
	
	class Meta:
		verbose_name = '商品属性定义'
		verbose_name_plural = '商品属性定义'

@python_2_unicode_compatible
class Product_Attribute(models.Model):
	product = models.ForeignKey(Product,null=True,related_name='attributes')
	sub_item_number = models.CharField(max_length = 100,default='',db_index=True)
	quantity = models.IntegerField(default=0)
	price_adjusment = models.FloatField()
	image = models.ForeignKey(Product_Images,null=True,blank=True)
	name = models.CharField(max_length = 254,default='')
	attribute = models.ManyToManyField(Attribute,null=True)
	min_order_quantity = models.IntegerField(default=0,verbose_name='最小下单数量')
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '商品属性'
		verbose_name_plural = '商品属性'


class Cart(models.Model):
	user = models.ForeignKey(MyUser,null=True,related_name='mycart')
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def get_sub_total(self):
		total = 0
		for cart_product in self.cart_products.all():
			total = total + cart_product.get_total()
		return total
	
class Cart_Products(models.Model):
	cart = models.ForeignKey(Cart,null=True,related_name='cart_products')
	product = models.ForeignKey(Product,null=True)
	product_attribute = models.ForeignKey(Product_Attribute,null=True)
	quantity = models.IntegerField(default=0)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def get_total(self):
		return self.quantity * self.get_product_price()
		
	def get_short_product_attr(self):
		logger.debug('product_attribute: %s' % self.product_attribute)
		attr_list = []
		if self.product_attribute:
			attr_list = Attribute.objects.filter(product_attribute=self.product_attribute).distinct()
		ret_str = ''
		for attr in attr_list:
			ret_str = ret_str + ' [' + attr.group.name + ':' + attr.name + ']'
		return ret_str
	
	def get_product_price(self):
		if self.product_attribute is None:
			return self.product.price
		else:
			return self.product_attribute.price_adjusment + self.product.price

	
class Wish(models.Model):
	user = models.ForeignKey(MyUser,null=True,related_name='wishs')
	product = models.ForeignKey(Product,null=True)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)

class Email(models.Model):
	useage = models.CharField(max_length = 100,unique=True)
	email_address = models.EmailField(null=True)
	title = models.CharField(max_length=254,verbose_name='邮件主题')
	smtp_host = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	template = models.CharField(max_length=254,null=True,blank=True,verbose_name='模板组名称')
	template_file = models.CharField(max_length=254,null=True,blank=True,verbose_name='模板文件名称')
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)

@python_2_unicode_compatible
class Order(models.Model):
	# 订单等待付款 
	ORDER_STATUS_PLACE_ORDER = '0' 
	# 订单已付款，等待确认 
	ORDER_STATUS_PAYED_UNCONFIRMED = '5'
	# 订单付款已确认
	ORDER_STATUS_PAYED_SUCCESS = '10'
	# 订单已发货
	ORDER_STATUS_SHIPPING = '20'
	# 订单已完成
	ORDER_STATUS_COMPLETE = '30'
	# 订单已取消
	ORDER_STATUS_CANCLED = '40'
	# 订单异常
	ORDER_STATUS_ERROR = '90'
	# 订单已关闭
	ORDER_STATUS_CLOSED = '99'
	# 文章状态选项 
	ORDER_STATUS_CHOICES = ( 
		(ORDER_STATUS_PLACE_ORDER,'等待付款'),
		(ORDER_STATUS_PAYED_UNCONFIRMED,'已付款未确认'),
		(ORDER_STATUS_PAYED_SUCCESS,'已付款'),
		(ORDER_STATUS_SHIPPING,'已发货'),
		(ORDER_STATUS_COMPLETE,'已完成'),
		(ORDER_STATUS_CANCLED,'已取消'),
		(ORDER_STATUS_ERROR,'订单异常'),
		(ORDER_STATUS_CLOSED,'订单已关闭')
	) 


	order_number = models.CharField(max_length = 100,unique=True,db_index=True,verbose_name='订单编号')
	user = models.ForeignKey(MyUser,null=True,related_name='orders',verbose_name='用户')
	status = models.CharField(max_length = 32,default='0',verbose_name='订单状态',choices=ORDER_STATUS_CHOICES)
	shipping_status = models.CharField(max_length = 100,default='not yet',blank=True,verbose_name='发货状态')
	pay_status = models.CharField(max_length = 100,default='wait for payment',blank=True)
	country = models.CharField(max_length = 100,default='',blank=True,verbose_name='国家')
	province = models.CharField(max_length = 100,default='',blank=True,verbose_name='省/州')
	city = models.CharField(max_length = 100,default='',blank=True,verbose_name='市')
	district = models.CharField(max_length = 100,default='',blank=True,verbose_name='区')
	address_line_1 = models.CharField(max_length = 254,default='',blank=True,verbose_name='地址 1')
	address_line_2 = models.CharField(max_length = 254,default='',blank=True,verbose_name='地址 2')
	first_name = models.CharField(max_length = 254,default='',blank=True,verbose_name='名')
	last_name = models.CharField(max_length = 254,default='',blank=True,verbose_name='姓')
	zipcode = models.CharField(max_length = 10,default='',blank=True,verbose_name='邮编')
	tel = models.CharField(max_length = 20,default='',blank=True,verbose_name='电话')
	mobile = models.CharField(max_length = 20,default='',blank=True)
	email = models.CharField(max_length = 100,default='',blank=True)
	express_type_name = models.CharField(max_length=100,null=True,blank=True,verbose_name='送货方式')
	shipper_name = models.CharField(max_length = 100,default='',blank=True,verbose_name='快递名称')
	shpping_no = models.CharField(max_length = 100,default='',blank=True,verbose_name='快递单号')
	pay_id = models.CharField(max_length = 100,default='',blank=True)
	pay_name = models.CharField(max_length = 100,default='',blank=True)
	products_amount = models.FloatField(default=0.00)
	shipping_fee = models.FloatField(default=0.00)
	discount = models.FloatField(default=0.00)
	order_amount = models.FloatField(default=0.00,verbose_name='订单总价')
	money_paid = models.FloatField(default=0.00)
	refer = models.CharField(max_length = 10,default='',blank=True)
	pay_time = models.DateTimeField(null=True)
	shipping_time = models.DateTimeField(null=True)
	to_seller = models.CharField(max_length = 100,blank=True)
	create_time = models.DateTimeField(auto_now_add = True,verbose_name='下单日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name='更新日期')

	def __str__(self):
		return self.order_number
	
	def get_human_status(self):
		dict = {'0':'Wait For Payment','10':'Wait For Shipment','20':'Shipping','30':'Complete','40':'Canceled','90':'Payment Error','99':'Closed'}
		return dict[self.status]
	#get_human_status.admin_order_field = 'pub_date'
	#get_human_status.boolean = True
	get_human_status.short_description = '订单状态'
	
	class Meta:
		verbose_name = '订单'
		verbose_name_plural = '订单'

@python_2_unicode_compatible		
class OrderRemark(models.Model):
	order = models.ForeignKey(Order,null=True,related_name='order_remarks')
	content = models.CharField(max_length=254,null=True,blank=True,verbose_name='备注内容')
	user = models.ForeignKey(MyUser,null=True,related_name='order_remarks')
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		return self.content
	
	class Meta:
		verbose_name = '订单备注'
		verbose_name_plural = '订单备注'
	

@python_2_unicode_compatible		
class Order_Products(models.Model):
	product_id = models.IntegerField(default=0,verbose_name='商品编号')
	product_attribute = models.ForeignKey(Product_Attribute,null=True)
	order = models.ForeignKey(Order,null=True,related_name='order_products')
	name = models.CharField(max_length = 100,default='',verbose_name='商品名称')
	short_desc = models.CharField(max_length = 254,default='')
	price = models.FloatField(verbose_name='商品价格')
	thumb = models.URLField()
	image = models.URLField()
	quantity = models.IntegerField(default=0,verbose_name='订购数量')
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)
	
	def get_total(self):
		return self.quantity * self.price
	get_total.short_description = '金额小计'
	
	def __str__(self):
		return self.name
		
	def get_short_product_attr(self):
		attr_list = []
		if self.product_attribute:
			attr_list = Attribute.objects.filter(product_attribute=self.product_attribute).distinct()
		ret_str = ''
		for attr in attr_list:
			ret_str = ret_str + ' [' + attr.group.name + ':' + attr.name + ']'
		return ret_str
	
	class Meta:
		verbose_name = '订单商品'
		verbose_name_plural = '订单商品'

class Abnormal_Order(models.Model):
	order = models.ForeignKey(Order,null=True,related_name='abnormal_orders')
	reason = models.CharField(max_length=100,null=True)
	detail = models.TextField()
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)

class Reset_Password(models.Model):
	email = models.EmailField('email address',max_length=254)
	validate_code = models.CharField(max_length=254)
	is_active = models.BooleanField(default=False)
	apply_time = models.DateTimeField()
	expirt_time = models.DateTimeField()
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)

class Serial_Number(models.Model):
	work_date = models.CharField(max_length=8,unique=True)
	serial_number = models.IntegerField(default=1)
	create_time = models.DateTimeField(auto_now_add = True)
	update_time = models.DateTimeField(auto_now = True)

	
@python_2_unicode_compatible
class Article(models.Model):
	title = models.CharField(max_length=254,null=True,db_index=True,verbose_name = '标题')
	# 博客类宣传文章
	ARTICLE_CATEGORY_BLOG = '0' 
	# 公告类文章
	ARTICLE_CATEGORY_NOTICE = '10'
	# 网站信息文章
	ARTICLE_CATEGORY_SITEINFO = '20'
	# 文章状态选项 
	CATEGORY_CHOICES = ( 
		(ARTICLE_CATEGORY_BLOG,'宣传博客'),
		(ARTICLE_CATEGORY_NOTICE,'网站公告'),
		(ARTICLE_CATEGORY_SITEINFO,'站点信息'),
	) 
	category = models.CharField(max_length=10,null=True,blank=True,verbose_name = '文章分类',choices=CATEGORY_CHOICES)
	content = models.TextField(null=True,blank=True,verbose_name = '内容')
	user = models.ForeignKey(MyUser,null=True,blank=True,verbose_name = '用户')
	keywords = models.CharField(max_length=254,null=True,blank=True,verbose_name = '关键字')
	page_title = models.CharField(max_length = 100,blank=True,default='',verbose_name='网页标题')
	short_desc = models.CharField(max_length = 254,default='',blank=True,verbose_name='简略描述')
	static_file_name = models.CharField(max_length = 254,db_index=True,unique=True,null=True,blank=True,verbose_name = '静态文件名')
	folder = models.CharField(max_length = 254,null=True,blank=True,verbose_name = '静态文件目录')
	breadcrumbs = models.CharField(max_length = 254,null=True,blank=True,verbose_name = '导航位置')
	image = models.URLField(null=True,blank=True,verbose_name = '图片链接')
	detail_template = models.CharField(max_length = 254,default='',blank=True,verbose_name='详情页指定模板')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新日期')
	
	def __str__(self):
		return self.title
	
	def get_url(self):
		from shopcart.functions.article_util_func import get_url
		return get_url(self)

	class Meta:
		verbose_name = '文章'
		verbose_name_plural = '文章'

class Album(models.Model):
	item_type = models.CharField(max_length=100,verbose_name = '对象类型')
	item_id = models.IntegerField(default=0,verbose_name = '对象ID')
	image = models.URLField(verbose_name = '图片链接')
	thumb = models.URLField(verbose_name = '缩略图链接')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新日期')
	
	class Meta:
		verbose_name = '相册'
		verbose_name_plural = '相册'
	
@python_2_unicode_compatible
class Email_List(models.Model):
	email = models.EmailField(unique=True, db_index=True, max_length=254,verbose_name = '电子邮件')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新日期')
	
	def __str__(self):
		return self.email
		
	class Meta:
		verbose_name = '订阅邮件列表'
		verbose_name_plural = '订阅邮件列表'

@python_2_unicode_compatible
class ExpressType(models.Model):
	name = models.CharField(max_length=100,null=True,verbose_name = '送货方式')
	price_fixed = models.FloatField(verbose_name = '固定运费')
	price_per_kilogram = models.FloatField(verbose_name = '每千克运费')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新日期')
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '送货方式'
		verbose_name_plural = '送货方式'

		
@python_2_unicode_compatible
class Express(models.Model):
	name = models.CharField(max_length=100,null=True,verbose_name = '快递名称')
	express_type = models.ManyToManyField(ExpressType,null=True,related_name='expresses')
	price_fixed = models.FloatField(verbose_name = '固定运费')
	price_per_kilogram = models.FloatField(verbose_name = '每千克运费')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新日期')
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '快递公司'
		verbose_name_plural = '快递公司'
			

@python_2_unicode_compatible		
class Inquiry(models.Model):
	name = models.CharField(max_length=100,null=True,verbose_name = '对方称呼')
	company = models.CharField(max_length=200,null=True,verbose_name = '对方公司')
	email = models.EmailField(max_length=254,null=True,verbose_name = '电子邮件')
	message = models.TextField(blank=True,verbose_name='询盘信息')
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新日期')
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = '询盘信息'
		verbose_name_plural = '询盘信息'

		
@python_2_unicode_compatible			
class Promotion(models.Model):
	code = models.CharField(max_length=100,db_index=True,verbose_name='促销码')
	is_reuseable = models.BooleanField(verbose_name='可否重复使用')
	is_valid = models.BooleanField(verbose_name='是否有效')
	valid_date_begin = models.DateTimeField(verbose_name='有效期开始时间')
	valid_date_end = models.DateTimeField(verbose_name='有效期结束时间')
	
	DISCOUNT_TYPE_FIXED = 'FIXED'
	DISCOUNT_TYPE_SCALE = 'SCALE'
	DISCOUNT_TYPE_OFF_WHEN_UPTOX = 'OFF_WHEN_UPTOX'
	DISCOUNT_TYPE_FREE_SHIPPING = 'FREE_SHIPPING'
	DISCOUNT_TYPE_FUNCTION = 'FUNCTION'
	DISCOUNT_TYPE_CHOICES = ( 
		(DISCOUNT_TYPE_FIXED,'固定优惠'),
		(DISCOUNT_TYPE_SCALE,'百分比'),
		(DISCOUNT_TYPE_OFF_WHEN_UPTOX,'满减'),
		(DISCOUNT_TYPE_FREE_SHIPPING,'免邮费'),
		(DISCOUNT_TYPE_FUNCTION,'公式自定义'),
	)
	
	discount_condition = models.CharField(max_length=255,null=True,blank=True,verbose_name='优惠条件(表达式)')
	
	discount_type = models.CharField(max_length=20,verbose_name='优惠方式')
	discount = models.CharField(max_length=255,verbose_name='优惠额或公式')
	
	item_type = models.CharField(null=True,blank=True,max_length=20,verbose_name='优惠对象类型')
	item_id = models.IntegerField(null=True,blank=True,verbose_name='优惠对象ID')
	
	impl_class = models.CharField(null=True,blank=True,max_length=255,verbose_name='优惠插件名称')	
	
	create_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建日期')
	update_time = models.DateTimeField(auto_now = True,verbose_name = '更新日期')
	
	def __str__(self):
		return self.code
	
	class Meta:
		verbose_name = '促销代码'
		verbose_name_plural = '促销代码'