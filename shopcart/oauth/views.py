# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.db import transaction
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from shopcart.utils import get_system_parameters
from shopcart.models import OAuthSite

import logging
logger = logging.getLogger('icetus.shopcart')

from shopcart.oauth import SocialSites, SocialAPIError



def callback(request,sitename):
	code = request.GET.get('code')
	logger.info('code : %s' % code)
	if not code:
		return redirect('/oautherror')

	socialsites = SocialSites()
	s = socialsites.get_site_object_by_name('wechat')
	try:
		logger.info('Start to get token... ')
		s.SCOPE = 'snsapi_userinfo'
		s.get_access_token(code)
		logger.info('Token has been getted.')
	except SocialAPIError as err:
		# 这里可能会发生错误
		logger.error('%s %s %s oAuth Error. \n Error Message: %s ' % (e.site_name,e.url,e.error_msg))      # 哪个站点的OAuth2发生错误？
		raise

	# 到这里授权完毕，并且取到了用户信息，uid, name, avatar...
	logger.info('username : %s ' % s.name)
	return HttpResponse('用户uid：%s , 用户名：%s , avater:<img src="%s" >' % (s.uid,s.name,s.avatar))	
	
	
	
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
		
		
class WechatCheckSign:
	"""
	用于微信校验用户服务是否可用的类，根据微信接口，校验微信的signatur。
	调用者先用从URL中得到的参数，实例化本类，然后调用is_valid方法校验，如果结果为True，则返回echostr，否则随便返回一个值。
	"""
	def __init__(self,timestamp,nonce,echostr,signature):
		wechat =  OAuthSite.objects.get(name='wechat')
		self.ret = {
			'app_id':wechat.client_id,
			'timestamp':timestamp,
			'nonce':nonce,
			'echostr':echostr,
			'token':'icetusweixinlogin',
			'signature':signature,
			#'wechat_api_url':System_Config.objects.get(name='wechat_api_url').val,
			#'wechat_api_port':System_Config.objects.get(name='wechat_api_port').val
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