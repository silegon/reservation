#coding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^order_cancel$', 'dish.j.views.order_cancle'),
                       url(r'^order_finish$', 'dish.j.views.order_finish'),
                       url(r'^order_book_confirm$', 'dish.j.views.order_book_confirm'),
                       url(r'^confirm_order', 'dish.j.views.confirm_order'),
                       url(r'^finish_order', 'dish.j.views.finish_order'),
                       url(r'^food_list$', 'dish.j.views.food_list'),
                       url(r'^new_food', 'dish.j.views.new_food'),
                      )
