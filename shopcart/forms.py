# -*- coding:utf-8 -*-
from django import forms
from shopcart.models import MyUser, Address, Product, Inquiry, OrderShippment, Email, Article, Express, ExpressType, \
    Category, CustomizeURL, ArticleBusiCategory, ProductParaGroup, Attribute_Group, Slider, Promotion, ProductPushGroup, \
    Recruit
from captcha.fields import CaptchaField
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class push_group_detail_form(forms.ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = ProductPushGroup
        fields = ('name', 'code')


class promotion_detail_form(forms.ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = Promotion
        fields = (
            'name', 'code', 'discount_type', 'discount', 'valid_date_begin', 'valid_date_end', 'is_reuseable',
            'is_valid')


class slider_detail_form(forms.ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = Slider
        fields = ('name', 'code')


class product_sku_group_form(forms.ModelForm):
    class Meta:
        model = Attribute_Group
        fields = ('name', 'code', 'group_type')


class product_para_group_form(forms.ModelForm):
    class Meta:
        model = ProductParaGroup
        fields = ('name',)


class article_busi_category_form(forms.ModelForm):
    name = forms.CharField(required=False)
    code = forms.CharField(required=False)
    sort_order = forms.CharField(required=False)
    keywords = forms.CharField(required=False)

    page_title = forms.CharField(required=False)
    static_file_name = forms.CharField(required=False)
    short_desc = forms.CharField(required=False)
    category_template = forms.CharField(required=False)

    class Meta:
        model = ArticleBusiCategory
        fields = (
            'name', 'code', 'sort_order', 'keywords', 'page_title', 'static_file_name', 'short_desc',
            'category_template')


# 只验证captcha字段的form
class captcha_form(forms.Form):
    # 暂时什么都不校验
    # captcha = CaptchaField()
    pass


class register_form(forms.ModelForm):
    # captcha = CaptchaField(),新版暂时不要验证码
    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name')


class user_info_form(forms.ModelForm):
    # captcha = CaptchaField(),新版暂时不要验证码
    password = forms.CharField(required=False)

    class Meta:
        model = MyUser
        fields = ('password', 'first_name', 'last_name')


class address_form(forms.ModelForm):
    tel = forms.CharField(required=False)
    mobile = forms.CharField(required=False)
    sign_building = forms.CharField(required=False)
    useage = forms.CharField(required=False)

    class Meta:
        model = Address
        fields = (
            'useage', 'is_default', 'first_name', 'last_name', 'country', 'province', 'city', 'district',
            'address_line_1',
            'address_line_2', 'zipcode', 'tel', 'mobile', 'sign_building')


class product_add_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('item_number', 'name')


class product_basic_info_form(forms.ModelForm):
    keywords = forms.CharField(required=False)
    youtube = forms.CharField(required=False)
    static_file_name = forms.CharField(required=False)
    page_title = forms.CharField(required=False)
    short_desc = forms.CharField(required=False)
    type = forms.CharField(required=False)
    sort_order = forms.CharField(required=False)

    class Meta:
        model = Product
        # fields = ('item_number','name','is_publish','price','market_price','quantity','min_order_quantity')
        fields = ('item_number', 'name', 'youtube', 'keywords', 'page_title', 'static_file_name', 'type', 'short_desc',
                  'sort_order', 'is_publish')


class product_detail_info_form(forms.ModelForm):
    market_price = forms.CharField(required=False)
    detail_template = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = Product
        fields = (
            'market_price', 'quantity', 'min_order_quantity', 'weight', 'cuboid_long', 'cuboid_width', 'cuboid_height',
            'detail_template', 'description')


class article_basic_info_form(forms.ModelForm):
    keywords = forms.CharField(required=False)
    page_title = forms.CharField(required=False)
    sort_order = forms.CharField(required=False)
    short_desc = forms.CharField(required=False)
    static_file_name = forms.CharField(required=False)
    detail_template = forms.CharField(required=False)
    breadcrumbs = forms.CharField(required=False)

    class Meta:
        model = Article
        fields = ('title', 'sort_order', 'keywords', 'page_title', 'short_desc', 'static_file_name', 'breadcrumbs',
                  'detail_template', 'category')


class article_detail_info_form(forms.ModelForm):
    content = forms.CharField(required=False)

    class Meta:
        model = Product
        fields = ('content',)


class order_shippment_form(forms.ModelForm):
    shipper_name = forms.CharField(required=False)
    ship_no = forms.CharField(required=False)
    shipping_cost = forms.CharField(required=False)
    shipping_time = forms.CharField(required=False)
    remark = forms.CharField(required=False)
    country = forms.CharField(required=False)
    province = forms.CharField(required=False)
    city = forms.CharField(required=False)
    district = forms.CharField(required=False)
    address_line_1 = forms.CharField(required=False)
    address_line_2 = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    zipcode = forms.CharField(required=False)
    tel = forms.CharField(required=False)

    class Meta:
        model = OrderShippment
        fields = ('shipper_name', 'ship_no', 'shipping_cost', 'shipping_time', 'remark', 'country', 'province', 'city',
                  'district', 'address_line_1', 'address_line_2', 'first_name', 'last_name', 'zipcode', 'tel')


class email_form(forms.ModelForm):
    useage_name = forms.CharField(required=False)
    is_send = forms.CharField(required=False)
    need_ssl = forms.CharField(required=False)
    email_address = forms.CharField(required=False)
    title = forms.CharField(required=False)
    smtp_host = forms.CharField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)
    template = forms.CharField(required=False)
    template_file = forms.CharField(required=False)

    class Meta:
        model = Email
        fields = ('useage_name', 'is_send', 'email_address', 'title', 'smtp_host', 'username', 'password', 'template',
                  'template_file', 'need_ssl')


class category_simple_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'code', 'sort_order')


class category_form(forms.ModelForm):
    name = forms.CharField(required=False)
    code = forms.CharField(required=False)
    page_title = forms.CharField(required=False)
    keywords = forms.CharField(required=False)
    short_desc = forms.CharField(required=False)
    description = forms.CharField(required=False)
    sort_order = forms.CharField(required=False)
    detail_template = forms.CharField(required=False)
    category_template = forms.CharField(required=False)
    static_file_name = forms.CharField(required=False)

    class Meta:
        model = Category
        fields = (
            'name', 'code', 'page_title', 'keywords', 'short_desc', 'sort_order', 'description', 'detail_template',
            'category_template', 'static_file_name')


class express_form(forms.ModelForm):
    class Meta:
        model = Express
        fields = ('name', 'is_in_use', 'price_fixed')


class express_type_form(forms.ModelForm):
    class Meta:
        model = ExpressType
        fields = ('name', 'is_in_use', 'price_fixed', 'price_per_kilogram', 'price_per_stere', 'price_calc_type')


class inquiry_form(forms.ModelForm):
    company = forms.CharField(required=False)
    name = forms.CharField(required=False)
    product = forms.CharField(required=False)
    quantity = forms.CharField(required=False)
    unit = forms.CharField(required=False)
    title = forms.CharField(required=False)

    class Meta:
        model = Inquiry
        fields = ('name', 'company', 'email', 'message', 'product', 'quantity', 'unit', 'title')


class customize_url_detail_form(forms.ModelForm):
    target_url = forms.CharField(required=False)
    keywords = forms.CharField(required=False)
    short_desc = forms.CharField(required=False)

    class Meta:
        model = CustomizeURL
        fields = ('url', 'target_url', 'type', 'is_customize_tdk', 'page_name', 'keywords', 'short_desc')


class recruit_basic_info_form(forms.ModelForm):
    keywords = forms.CharField(required=False)
    sort_order = forms.CharField(required=False)
    static_file_name = forms.CharField(required=False)
    content = forms.CharField(required=False)
    class Meta:
        model = Recruit
        fields = ('title', 'sort_order', 'keywords', 'content', 'number', 'education', 'site', 'type','static_file_name',)


# class recruit_detail_info_form(forms.ModelForm):
#     content = forms.CharField(required=False)
#
#     class Meta:
#         model = Recruit
#         fields = ('content',)
