# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-30 05:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderShippment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipper_name', models.CharField(blank=True, max_length=254, null=True, verbose_name='快递公司')),
                ('ship_no', models.CharField(blank=True, max_length=254, null=True, verbose_name='快递单号')),
                ('shipping_cost', models.FloatField(default=0.0, verbose_name='快递成本')),
                ('shipping_time', models.DateTimeField(null=True, verbose_name='发货时间')),
                ('remark', models.CharField(blank=True, max_length=254, null=True, verbose_name='备注')),
                ('country', models.CharField(blank=True, default='', max_length=100, verbose_name='国家')),
                ('province', models.CharField(blank=True, default='', max_length=100, verbose_name='省/州')),
                ('city', models.CharField(blank=True, default='', max_length=100, verbose_name='市')),
                ('district', models.CharField(blank=True, default='', max_length=100, verbose_name='区')),
                ('address_line_1', models.CharField(blank=True, default='', max_length=254, verbose_name='地址 1')),
                ('address_line_2', models.CharField(blank=True, default='', max_length=254, verbose_name='地址 2')),
                ('first_name', models.CharField(blank=True, default='', max_length=254, verbose_name='名')),
                ('last_name', models.CharField(blank=True, default='', max_length=254, verbose_name='姓')),
                ('zipcode', models.CharField(blank=True, default='', max_length=10, verbose_name='邮编')),
                ('tel', models.CharField(blank=True, default='', max_length=20, verbose_name='电话')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '发货记录',
                'verbose_name_plural': '发货记录',
            },
        ),
        migrations.RemoveField(
            model_name='order_products',
            name='product_attribute',
        ),
        migrations.AddField(
            model_name='email',
            name='is_send',
            field=models.BooleanField(default=False, verbose_name='是否发送'),
        ),
        migrations.AddField(
            model_name='email',
            name='useage_name',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='邮件用途显示名称'),
        ),
        migrations.AddField(
            model_name='express',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='express',
            name='is_in_use',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
        migrations.AddField(
            model_name='expresstype',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='expresstype',
            name='is_in_use',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='ip_address',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='IP地址'),
        ),
        migrations.AddField(
            model_name='order_products',
            name='product_attribute_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='SKU的id'),
        ),
        migrations.AddField(
            model_name='order_products',
            name='product_attribute_item_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='SKU编号'),
        ),
        migrations.AddField(
            model_name='order_products',
            name='product_attribute_name',
            field=models.CharField(default='', max_length=1000, verbose_name='选中的商品属性文字说明'),
        ),
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, null=True, related_name='_product_related_products_+', to='shopcart.Product', verbose_name='关联商品'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='thumb',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('0', '等待付款'), ('5', '已付款未确认'), ('10', '已付款'), ('15', '已备货'), ('20', '已发货'), ('30', '已完成'), ('40', '已取消'), ('90', '订单异常'), ('99', '订单已关闭')], default='0', max_length=32, verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='product_attribute',
            name='attribute',
            field=models.ManyToManyField(null=True, related_name='product_attribute', to='shopcart.Attribute'),
        ),
        migrations.AlterField(
            model_name='product_attribute',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopcart.Product_Images'),
        ),
        migrations.AddField(
            model_name='ordershippment',
            name='express',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to='shopcart.Express', verbose_name='承运快递公司'),
        ),
        migrations.AddField(
            model_name='ordershippment',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippments', to='shopcart.Order'),
        ),
    ]
