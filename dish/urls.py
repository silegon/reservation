#coding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^j/', include('dish.j.urls')),
                       url(r'^register$', 'dish.views.register', name='register'),
                       url(r'^logout$', 'dish.views.logout', name='logout'),
                       url(r'^process_order$', 'dish.views.process_order', name='process_order'),
                       url(r'^records$', 'dish.views.records', name='records'),
                       url(r'^avatar$', 'dish.views.avatar', name='records'),
                       url(r'^login$', 'dish.views.login', name='login'),
                       url(r'^admin_login$', 'dish.views.admin_login', name='admin_login'),
                       url(r'^$', 'dish.views.menu', name='menu'),
                      )
