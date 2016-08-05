# -*- coding: UTF-8 –*-
# Create your views here.
from django.http import HttpResponse
from shopcart.models import System_Config
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
import http.client
import time
import random
import string
import hashlib
import json
import logging
logger = logging.getLogger('icetus.shopcart')


class WechatCheckSign:
	"""
	用于微信校验用户服务是否可用的类，根据微信接口，校验微信的signatur。
	调用者先用从URL中得到的参数，实例化本类，然后调用is_valid方法校验，如果结果为True，则返回echostr，否则随便返回一个值。
	"""
	def __init__(self,timestamp,nonce,echostr,signature):
		self.ret = {
			'app_id':System_Config.objects.get(name='wechat_app_id').val,
			'timestamp':timestamp,
			'nonce':nonce,
			'echostr':echostr,
			'token':System_Config.objects.get(name='wechat_token').val,
			'signature':signature,
			'wechat_api_url':System_Config.objects.get(name='wechat_api_url').val,
			'wechat_api_port':System_Config.objects.get(name='wechat_api_port').val
		}
		
	
	def is_valid(self):
		tmp_list = [self.ret['token'], self.ret['timestamp'], self.ret['nonce']]
		tmp_list.sort()
		tmp_str = "%s%s%s" % tuple(tmp_list)
	
		tmp_str = hashlib.sha1(tmp_str.encode('utf8')).hexdigest()
		logger.debug('Our signature:' %s (tmp_str))
		if tmp_str == self.ret['signature']:
			return True
		else:
			return False

			
class WechatLoginSign:
	def __init__(self,code):
		self.ret={
			'app_id':System_Config.objects.get(name='wechat_app_id').val,
			'code':code,
			'secret':System_Config.objects.get(name='wechat_app_secret').val,
			'wechat_api_url':System_Config.objects.get(name='wechat_api_url').val,
			'wechat_api_port':System_Config.objects.get(name='wechat_api_port').val
		}
			
	def login(self):
		app_id = self.ret['app_id']
		code = self.ret['code']
		secret = self.ret['secret']
		
		logger.debug('start to get access_token...')
		#用code换取access_tokon
		#https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
		url = '/sns/oauth2/access_token?appid=%(app_id)s&secret=%(secret)s&code=%(code)s&grant_type=authorization_code' % {'app_id':app_id,'secret':secret,'code':code}
		token_info = make_https_get_call(host=self.ret['wechat_api_url'],port=self.ret['wechat_api_port'],url=url,timeout=30)
		
		if not token_info:
			return False
		logger.debug('openid:%s' % (token_info['openid']))
		logger.debug('token:%s' % (token_info['access_token']))
		
		#拉取用户信息
		#https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
		logger.debug('start to get user info...')
		url = '/sns/userinfo?access_token=%(token)s&openid=%(openid)s&lang=zh_CN' % {'token':token_info['access_token'],'openid':token_info['openid']}
		logger.debug('url:%s' %(url))
		user_info = make_https_get_call(host=self.ret['wechat_api_url'],port=self.ret['wechat_api_port'],url=url,timeout=30)
		
		if not user_info:
			return False
		
		logger.debug('nickname:%s' %(user_info['nickname']))
		logger.debug('headimgurl:%s' % (user_info['headimgurl']))
		self.ret['wechat_nickname'] = user_info['nickname']
		self.ret['wechat_head_img_url'] = user_info['headimgurl']
		return True
			
class WechatOrderSign:
	"""
	微信统一下单接口类
	"""
	def __init__(self, pbody='',open_id='',out_trade_no='',spbill_create_ip='',total_fee=0,attach=''):
		#self.ret = {
		#	'nonce_str': self.__create_nonce_str(),
		#	'appid': System_Config.objects.get(name='wechat_app_id').val,
		#	'mch_id': System_Config.objects.get(name='wechat_mch_id').val,
		#	'body': body,
		#	'device_info':'WEB'
		#}
		logger.debug('1111:')
		pbody = '赋值了'
		pbody = 'my pbody'
		logger.debug(pbody)
		
		self.ret = {
			'nonce_str': self.__create_nonce_str(),
			'appid': System_Config.objects.get(name='wechat_app_id').val,
			'mch_id': System_Config.objects.get(name='wechat_mch_id').val,
			'body': '',
			'device_info':'WEB'
		}
		
		self.app = 'ni ge mai ti'

		logger.debug('self.ret:%s' % (self.ret))
		
		logger.debug('self.app:%s' % (self.app))
		
		self.other_parameters = {
			'attach':attach,
			'notify_url':System_Config.objects.get(name='wechat_notify_url').val,
			'open_id':open_id,
			'out_trade_no':out_trade_no,
			'spbill_create_ip':spbill_create_ip,
			'total_fee':total_fee,
			'trade_type':'JSAPI',
			'sign':''
		}
		
		logger.debug('self.other_parameters:' % (self.other_parameters))

		
	def __create_nonce_str(self):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

	def make_xml_parameters(self):
		xml = '<xml>'
		for key in self.ret:
			xml += '<' + key + '>' + str(self.ret[key]) + '</' + key + '>'
		for key in self.other_parameters:
			xml += '<' + key + '>' + str(self.other_parameters[key]) + '</' + key + '>'
		xml += '</xml>'
		logger.debug('xml:%s' % (xml))
		return xml		
		
	def sign(self):
		logger.debug('Enter sign...')
		
		
		logger.debug('self.ret:%s' % (self.ret))
		
		#string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
		#string = 'appid=%s&body=%s&device_info=%s&mch_id=%s&nonce_str=%s' % (self.ret['appid'],self.ret['body'],self.ret['device_info'],self.ret['mch_id'],self.ret['nonce_str'])
		string = 'nima'
		logger.debug('string:' + str(string))
		logger.debug('string:%s' % (string))
		
		
		mch_key = System_Config.objects.get(name='wechat_mch_key').val
		logger.debug('mch_key:%s' %(mch_key))
		#stringSignTemp=  '%s&key=%s' % (string,mch_key)
		#logger.debug('stringSignTemp:%s' % (stringSignTemp))
		
		#signature = hashlib.sha1(string.encode('utf8')).hexdigest()
		#signature = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
		#self.other_parameters['sign'] = signature
		#logger.debug('signature:%s' % (signature))
		#return signature

	
	def order(self):
		#https://api.mch.weixin.qq.com/pay/unifiedorder
		logger.debug('start to get sign...')
		self.sign()
		#param = self.make_xml_parameters()
		#logger.debug('param:' + str(param))
		
		"""
		httpClient = None
		try:
			host = 'api.mch.weixin.qq.com'
			port = 443
			httpClient = http.client.HTTPSConnection(host, port, timeout=30)
			
			header = {"Content-type": "text/xml", }
			httpClient.request("POST", '/pay/unifiedorder', param.encode('utf8'), header)
			#httpClient.request('POST', url)
			response = httpClient.getresponse()
			logger.debug('response.status:%s' %(response.status))
			logger.debug('response.reason:%s' %(response.reason))
			response_body = response.read()
			logger.debug('response.read():%s' %(response_body))
			
		except Exception as err:
			logger.error('Make Https Call to %s %s faild.' % (host,port))
			logger.error(str(err))
		finally:
			if httpClient:
				httpClient.close()
		"""
			
			
	
class WechatJSSDKSign:
	"""
	微信的JSSDK API需要用到的加密接口
	转发API用于用户点击微信浏览器中的“分享到朋友圈”、“分享给朋友”等按钮被点击时，会触发的方法，可以自定义转发的图标、标题和链接，
	并且，可以捕获用户"点击分享按钮"的事件、"分享成功"的事件、"分享取消"的事件
	"""
	def __init__(self,url):
		self.ret = {
			'nonceStr': self.__create_nonce_str(),
			'jsapi_ticket': '',
			'timestamp': self.__create_timestamp(),
			'url': url
		}
		self.app_id = System_Config.objects.get(name='wechat_app_id').val
		logger.debug('self.app_id：' + str(self.app_id))
		self.secret = System_Config.objects.get(name='wechat_app_secret').val
		self.wechat_api_url = System_Config.objects.get(name='wechat_api_url').val
		self.wechat_api_port = System_Config.objects.get(name='wechat_api_port').val

		logger.debug('JSSDK self.ret:%s' % (self.ret))
	def __create_nonce_str(self):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

	def __create_timestamp(self):
		return int(time.time())

	def get_ticket(self):
		url = '/cgi-bin/token?grant_type=client_credential&appid=%(app_id)s&secret=%(secret)s' % {'app_id':self.app_id,'secret':self.secret}
		logger.debug('url:%s' % (url))
		token_info = make_https_get_call(host=self.wechat_api_url,port=self.wechat_api_port,url=url,timeout=30)
			
		if not token_info:
			return ''
		
		url = '/cgi-bin/ticket/getticket?access_token=%(token)s&type=jsapi' % {'token':token_info['access_token']}
		logger.debug('url:%s' %(url))
			
		ticket_info = make_https_get_call(host=self.wechat_api_url,port=self.wechat_api_port,url=url,timeout=30)
		logger.debug('ticket:%s' % (ticket_info))
		
		if not ticket_info:
			return ''
		
		self.ret['jsapi_ticket'] = ticket_info['ticket']
		return ticket_info['ticket']

	def make_wechat_config(self):
		config_str = 'wx.config({debug:%(debug)s,appId:"%(appid)s",timestamp:%(timestamp)s,nonceStr:"%(nonce)s",signature:"%(signature)s",jsApiList:["checkJsApi","chooseWXPay","onMenuShareAppMessage","onMenuShareTimeline"]});' % {'debug':'true','appid':self.app_id,'timestamp':self.ret['timestamp'],'nonce':self.ret['nonceStr'],'signature':self.ret['signature']}
		return config_str 
		
	def sign(self):
		ticket = self.get_ticket()
		string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
		logger.debug('string:%s' % (string))
		signature = hashlib.sha1(string.encode('utf8')).hexdigest()
		self.ret['signature'] = signature
		logger.debug('signature:%s' % (signature))
		return self.make_wechat_config()
		
		

		
class WechatPaySign:
	"""
	微信支付加密类
	"""
	def __init__(self,app_id='',body='',mch_id='',open_id='',out_trade_no='',
		total_fee='',spbill_create_ip='',notify_url='',attach='',sign=''):
		self.ret = {
			'appid':app_id,
			'attach':attach,
			'body':body,
			'mch_id':mch_id,
			'nonce_str':self.__create_nonce_str(),
			'notify_url':notify_url,
			'openid':open_id,
			'out_trade_no':out_trade_no,
			'spbill_create_ip':spbill_create_ip,
			'total_fee':total_fee,
			'trade_type':'JSAPI',
			'sign':sign
		}
	
	def __create_nonce_str(self):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

		

@csrf_exempt
def wechat_check(request):
	"""
	微信公众号中，如果要接入用户自定义开发的网站，会有一个检测按钮，检测按钮会使用这个方法来检查用户是否能够正确返回。
	"""
	if request.method == "GET":
		signature = request.GET.get('signature','')
		timestamp = request.GET.get('timestamp','')
		nonce = request.GET.get('nonce','')
		echostr = request.GET.get('echostr','')
		
		logger.debug('signature:%s' %(signature))
		logger.debug('timestamp:%s' %(timestamp))
		logger.debug('nonce:%s' %(nonce))
		logger.debug('echostr:%s' %(echostr))
		
		check_sign = WechatCheckSign(timestamp=timestamp,nonce=nonce,echostr=echostr,signature=signature)
		
		if check_sign.is_valid:
			return HttpResponse(check_sign.ret['echostr'])
		else:
			return HttpResponse('Not Auth')
	else:
		raise Http404


def wechat_pay(request,id=''):	
	#1、通过统一下单接口下单
	logger.debug('id:%s' % (id))
	order = WechatOrderSign(pbody='这里是Body', attach='这里是Attach',open_id='oL-pIwLztIl8kJjk63Ky-e_Inekg',out_trade_no='OrderNo is 20160608',spbill_create_ip='127.0.0.1',total_fee=1)					
	order.order()
	return HttpResponse('OK')


	
@csrf_exempt
def wechat_login(request):
	code = request.GET.get('code','')
	logger.debug('从URL中获得的code:%s' % (code))
	login_sign = WechatLoginSign(code)
	if login_sign.login():
		#登陆成功
		
		#TODO：做本地登录动作
		return HttpResponse('<p>用户名：%s</p><p><img src="%s" /></p>' %(login_sign.ret['wechat_nickname'],login_sign.ret['wechat_head_img_url']))
	else:
		return HttpResponse('登陆失败')
	
	
	
def	make_https_get_call(host,port,url,timeout,return_type='json'):
	"""
	公共的https接口调用方法，入参有主机、端口、超时时间，返回类型：json,origin
	"""
	httpClient = None
	try:
		httpClient = http.client.HTTPSConnection(host, port, timeout=30)
		httpClient.request('GET', url)
		response = httpClient.getresponse()
		logger.debug('response.status:%s' %(response.status))
		logger.debug('response.reason:%s' %(response.reason))
		response_body = response.read()
		logger.debug('response.read():%s' %(response_body))
		
		if return_type == 'json':
			decode_ret = json.loads((response_body).decode())
			logger.debug('decode_ret:%s' % (decode_ret))
			return decode_ret
		elif return_type == 'origin':
			return response_body
		else:
			logger.error('The return_type %s is not support' % (return_type))
			return None
	except Exception as err:
		logger.error('Make Https Call to %s %s faild.' % (host,port))
		logger.error(str(err))
	finally:
		if httpClient:
			httpClient.close()

			
	
	
	
	
	
	