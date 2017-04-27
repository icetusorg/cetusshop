# -*- coding: utf-8 -*-


def import_oauth_class(m):
	print('m:%s' % m)
	m = m.split('.')
	c = m.pop(-1)
	print('m:%s,c:%s' % (m,c))
	module = __import__('.'.join(m), fromlist=[c])
	return getattr(module, c)
