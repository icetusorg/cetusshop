from __future__ import unicode_literals
from django.dispatch import Signal


# 用户注册的相关消息
user_registration_success = Signal(providing_args=['user'])


# 用户密码修改的相关消息
user_password_modify_applied = Signal(providing_args=['reset_password'])
user_password_modify_success = Signal(providing_args=['user'])

#商品的相关消息
product_added_to_cart = Signal(providing_args=['cart_id','product_id'])
product_added_to_wishlist = Signal(providing_args=['wish_id'])
product_price_changed = Signal(providing_args=['product_id','price_before','price_now'])
product_quantity_warn = Signal(providing_args=['product_id','product_attribute_id'])

#订单
order_was_placed = Signal(providing_args=['order'])
order_was_payed = Signal(providing_args=['order'])
order_was_canceled = Signal(providing_args=['order'])
order_was_shipped = Signal(providing_args=['order'])
order_was_complete = Signal(providing_args=['order'])

