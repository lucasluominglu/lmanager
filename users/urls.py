#coding=utf-8
'''为应用程序 user 定义的URL'''

from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

urlpatterns = [
	#login yemian
	url(r'^login/$', login, {'template_name':'users/login.html'}, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^register/$', views.register, name='register'),
]