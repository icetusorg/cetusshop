#coding=utf-8
from django.utils.translation import ugettext as _
import datetime,uuid

import logging
logger = logging.getLogger('icetus.shopcart')

def write_file(path='',filename=''):
	import xlwt
	style0=xlwt.easyxf('font:name Times New Roman,color-index red,bold on',num_format_str='#,##0.00')
	style1=xlwt.easyxf(num_format_str='DD-MM-YY')
	wb = xlwt.Workbook()
	ws = wb.add_sheet('A Test Sheet')
	ws.write(0,0,1234.56,style0)
	ws.write(1,0,datetime.datetime.now(),style1)
	ws.write(2, 0, 1)
	ws.write(2, 1, 1)
	wb.save('example.xls')
	return True

def read_file_demo():
	import xlrd
	fname = ".\media\import\product_import.xls"
	bk = xlrd.open_workbook(fname)
	shxrange = range(bk.nsheets)
	try:
		sh = bk.sheet_by_name("iCetus Products Export")
	except:
		logger.debug("no sheet in %s named 'iCetus Products Export'" % fname)
	#获取行数
	nrows = sh.nrows
	#获取列数
	ncols = sh.ncols
	logger.debug("nrows %d, ncols %d" % (nrows,ncols)) 
	#获取第一行第一列数据 
	cell_value = sh.cell_value(1,1)
	#print cell_value
	row_list = []
	#获取各行数据
	for i in range(1,nrows):
		row_data = sh.row_values(i)
		#logger.debug('row data:%s' % row_data)
		row_list.append(row_data)

	#logger.debug('Excel Data: %s' % row_list)
	return row_list
	
	
def export_products(product_list,file_name):
	import xlwt
	style_amount=xlwt.easyxf('font:name Times New Roman,color-index black,bold off',num_format_str='#,##0.00')
	
	wb = xlwt.Workbook()
	ws = wb.add_sheet('iCetus Products Export')
	#输出一行标题
	title_list = ['商品类型','产品名称','产品编号','URL','关键词','简要描述','分类','排序','上架','市场价','售价1','起订区间1','售价2','起订区间2','售价3','起订区间3','主图1','主图2','主图3','主图4','主图5','详细描述']
	
	
	for index,title in enumerate(title_list):
		ws.write(0,index,title)
	#输出商品对应的信息
	for index,p in enumerate(product_list):
		ws.write(index+1,0,p.type)
		ws.write(index+1,1,p.name)
		ws.write(index+1,2,p.item_number)
		ws.write(index+1,3,p.static_file_name)
		ws.write(index+1,4,p.keywords)
		ws.write(index+1,5,p.short_desc)
		
		cat_str = ''
		for cat in p.categorys.all():
			cat_str = cat_str + cat.name + ','
		if len(cat_str)>0:
			cat_str = cat_str[:-1]
		ws.write(index+1,6,cat_str)
		
		ws.write(index+1,7,p.sort_order)
		ws.write(index+1,8,p.is_publish)
		ws.write(index+1,9,p.market_price)
		
		
		price_list = []
		quantity_list = []
		for price in p.prices.all():
			price_list.append(price.price)
			quantity_list.append(price.quantity)
		p_count = len(price_list)
		for i in range(p_count,3):
			price_list.append('')
			quantity_list.append('')
		
		
		ws.write(index+1,10,price_list[0],style_amount)
		ws.write(index+1,11,quantity_list[0])
		ws.write(index+1,12,price_list[1],style_amount)
		ws.write(index+1,13,quantity_list[1])
		ws.write(index+1,14,price_list[2],style_amount)
		ws.write(index+1,15,quantity_list[2])
		
		image_list = []
		for img in p.get_main_image_list():
			image_list.append(img.image)
		count = len(image_list)
		for i in range(count,5):
			image_list.append('')
		
		ws.write(index+1,16,image_list[0])
		ws.write(index+1,17,image_list[1])
		ws.write(index+1,18,image_list[2])
		ws.write(index+1,19,image_list[3])
		ws.write(index+1,20,image_list[4])
		ws.write(index+1,21,p.description)
	wb.save('.\\' + file_name)	
	#wb.save('.\media\export\product_export.xls')
	return True
	

	