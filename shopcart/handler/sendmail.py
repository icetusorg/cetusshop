#coding=utf-8
from shopcart import signals
from django.utils.translation import ugettext as _
import logging
logger = logging.getLogger('icetus.shopcart')

#事件监听函数没法自动运行，需要被装载一下，现在是在主程序的__init__中使用了import功能触发

from django.dispatch import receiver
@receiver(signals.user_registration_success)
def user_registration_success_send_mail(sender, **kwargs):
	logger.info('Enter user_registration_success_send_mail hanlder!')
	from shopcart.utils import get_system_parameters
	user = kwargs['user']
	mail_ctx = {}
	mail_ctx['first_name'] = user.first_name
	mail_ctx['last_name'] = user.last_name
	mail_ctx['email'] = user.email
	mail_ctx['system_para'] = get_system_parameters()
		
	sendmail('user_registration_success_send_mail',user.email,mail_ctx,title=None,useage='user_registration_success')
	
@receiver(signals.user_password_modify_applied)			
def user_password_modify_applied_send_mail(sender,	**kwargs):
	logger.info('Enter user_password_modify_applied_send_mail hanlder!')
	email = kwargs['reset_password'].email
	validate_code = kwargs['reset_password'].validate_code
	mail_ctx = {}
	from shopcart.utils import get_system_parameters
	from shopcart.utils import url_with_out_slash
	mail_ctx['system_para'] = get_system_parameters()
	reset_url =  '%s/user/reset-password?email=%s&validate_code=%s' % (url_with_out_slash(mail_ctx['system_para']['base_url']),email,validate_code)
	logger.debug('reset_url:' + reset_url)
	mail_ctx['email'] = email
	mail_ctx['reset_password_link'] = reset_url
	
	sendmail('user_password_modify_applied_send_mail',email,mail_ctx,title=None,useage='user_password_modify_applied')
	

@receiver(signals.user_password_modify_success)
def user_password_modify_success_send_mail(sender,	**kwargs):
	logger.info('Enter user_password_modify_success_send_mail hanlder!')
	user = kwargs['user']
	mail_ctx = {}
	from shopcart.utils import get_system_parameters
	from shopcart.utils import url_with_out_slash
	mail_ctx['system_para'] = get_system_parameters()
	mail_ctx['first_name'] = user.first_name
	mail_ctx['last_name'] = user.last_name
	sendmail('user_password_modify_success_send_mail',user.email,mail_ctx,title=None,useage='user_password_modify_success')

@receiver(signals.product_added_to_cart)		
def product_added_to_cart_send_mail(sender,	**kwargs):
	logger.info('Enter product_added_to_cart_send_mail hanlder!')
	email = kwargs['email']
	mail_ctx = {}
	sendmail('user_registration_success_send_mail',email,mail_ctx,'')

@receiver(signals.product_added_to_wishlist)	
def product_added_to_wishlist_send_mail(sender,	**kwargs):
	logger.info('Enter product_added_to_wishlist_send_mail hanlder!')
	email = kwargs['email']
	mail_ctx = {}
	sendmail('user_registration_success_send_mail',email,mail_ctx,'')
			
@receiver(signals.order_was_placed)
def order_was_placed_send_mail(sender,	**kwargs):
	logger.info('Enter order_was_placed_send_mail hanlder!')
	email = kwargs['email']
	mail_ctx = {}
	sendmail('user_registration_success_send_mail',email,mail_ctx,'')

@receiver(signals.order_was_payed)
def order_was_payed_send_mail(sender,	**kwargs):
	logger.info('Enter order_was_payed_send_mail hanlder!')
	order = kwargs['order']
	user = order.user
	mail_ctx = {}
	from shopcart.utils import get_system_parameters
	mail_ctx['system_para'] = get_system_parameters()
	mail_ctx['first_name'] = user.first_name
	mail_ctx['last_name'] = user.last_name
	
	sendmail('order_was_payed_send_mail',user.email,mail_ctx,title=None,useage='order_was_payed')	
	
@receiver(signals.order_was_canceled)
def order_was_canceled_send_mail(sender,	**kwargs):
	logger.info('Enter order_was_canceled_send_mail hanlder!')
	email = kwargs['email']
	mail_ctx = {}
	sendmail('user_registration_success_send_mail',email,mail_ctx,'')
	
@receiver(signals.order_was_shipped)
def order_was_shipped_send_mail(sender,	**kwargs):
	logger.info('Enter order_was_shipped_send_mail hanlder!')
	email = kwargs['email']
	mail_ctx = {}
	sendmail('user_registration_success_send_mail',email,mail_ctx,'')
	
@receiver(signals.order_was_complete)
def order_was_complete_send_mail(sender,**kwargs):
	logger.info('Enter order_was_complete_send_mail hanlder!')
	email = kwargs['email']
	mail_ctx = {}
	sendmail('user_registration_success_send_mail',email,mail_ctx,'')	

#发送邮件	
def sendmail(type,email,mail_ctx,title,useage=type):
	logger.debug(type + ': Prepare to send mail.')
	if is_sendmail(type):
		logger.info('Mail [%s] has been sended to [%s].' % (type,email))
		from shopcart.utils import my_send_mail,url_with_out_slash
		from shopcart.models import Email
		email_definition = Email.objects.get(useage=useage)
		template = 'default'
		if email_definition.template != '' and email_definition.template != None:
			logger.debug('email.template is not none')
			template = url_with_out_slash(email_definition.template)
		
		template_file = useage + '.html'
		if email_definition.template_file != '' and email_definition.template_file != None:
			logger.debug('email.template_file is not none')
			template_file = template_file
		
		template_path =  'email/%s/%s' % (template,template_file)
		
		
		if title == None or title == '':
			from django.template import Context,loader,base
			title_template = base.Template(template_string = email_definition.title)
			title = title_template.render(Context(mail_ctx))
		logger.debug('Start to send mail.')
		my_send_mail(ctx=mail_ctx,send_to=email,title=title,template_path=template_path,username=email_definition.username,password=email_definition.password,smtp_host=email_definition.smtp_host,sender=email_definition.email_address)
		logger.debug('Send mail end.')
	else:
		logger.info('Mail function is closed.')	
			
#判断是都发送邮件，没有配置则不发送
def is_sendmail(type):
	from shopcart.models import System_Config
	try:
		item = System_Config.objects.get(name=type).val
		if item.lower() == 'true':
			return True
		else:
			return False
	except Exception as err:
		logger.info('System parameter [%s] is not defined. It will not send emails.' % (type))
		return False