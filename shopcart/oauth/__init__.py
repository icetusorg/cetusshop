# -*- coding: utf-8 -*-
from .exception import SocialSitesConfigError, SocialAPIError
from .utils import import_oauth_class
import logging
logger = logging.getLogger('icetus.shopcart')

def singleton(cls):
	instance = {}
	def get_instance(*args, **kwargs):
		if cls not in instance:
			instance[cls] = cls(*args, **kwargs)
		return instance[cls]
	return get_instance


@singleton
class SocialSites(object):
	"""This class holds the sites settings."""
	def __init__(self):
		self._configed = False
		self.config()

	def __getitem__(self, name):
		"""Get OAuth2 Class by it's setting name"""
		if not self._configed:
			raise SocialSitesConfigError("No configure")

		try:
			return self._sites_name_class_table[name]
		except KeyError:
			raise SocialSitesConfigError("No settings for site: %s" % name)

	def config(self):
		self._sites_name_class_table = {}
		# {'renren': 'socialoauth.sites.renren.RenRen',...}
		self._sites_class_config_table = {}
		# {'socialoauth.sites.renren.RenRen': {...}, ...}
		self._sites_name_list = []
		self._sites_class_list = []

		from shopcart.models import OAuthSite
		sites = OAuthSite.objects.all()
		
		for site in sites:
			self._sites_name_class_table[site.name] = site.name
			self._sites_class_config_table[site.impl_class] = {
				'site_name': site.name,
				#'site_name_zh': _site_name_zh,
			}
			
			self._sites_class_config_table[site.impl_class]['REDIRECT_URI'] = site.redirect_uri
			self._sites_class_config_table[site.impl_class]['CLIENT_ID'] = site.client_id
			self._sites_class_config_table[site.impl_class]['CLIENT_SECRET'] = site.client_secret
			self._sites_class_config_table[site.impl_class]['SCOPE'] = site.scope
			
			
			self._sites_name_list.append(site.name)
			self._sites_class_list.append(site.impl_class)
		
			print("_site_name:%s , %s" %(site.impl_class,self._sites_class_config_table[site.impl_class]))
		
		'''
		for _site_name, _site_class, _site_name_zh, _site_config in settings:
			self._sites_name_class_table[_site_name] = _site_class
			self._sites_class_config_table[_site_class] = {
				'site_name': _site_name,
				'site_name_zh': _site_name_zh,
		}
			print("_site_name:%s , %s" %(_site_class,self._sites_name_class_table[_site_name]))
			#for _k, _v in _site_config.iteritems():
			self._sites_class_config_table[_site_class]['REDIRECT_URI'] = 'http://www.lightstart.cn/account/oauth/wechat'
			self._sites_class_config_table[_site_class]['CLIENT_ID'] = '#'
			self._sites_class_config_table[_site_class]['CLIENT_SECRET'] = '#'
		'''	

			

		self._configed = True


	def load_config(self, module_class_name):
		"""
		OAuth2 Class get it's settings at here.
		Example:
			from socialoauth import socialsites
			class_key_name = Class.__module__ + Class.__name__
			settings = socialsites.load_config(class_key_name)
		"""
		logger.debug('_sites_class_config_table:%s' % self._sites_class_config_table)
		return self._sites_class_config_table[module_class_name]


	def list_sites_class(self):
		return self._sites_class_list
	
	def list_sites_name(self):
		return self._sites_name_list
	
	def get_site_object_by_name(self, site_name):
		site_class = self.__getitem__(site_name)
		print('site_class 1:%s' % site_class)
		return import_oauth_class(site_class)()
	
	def get_site_object_by_class(self, site_class):
		print('site_class 2:%s' % site_class)
		return import_oauth_class(site_class)()
