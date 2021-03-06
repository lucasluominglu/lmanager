from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
    url(r'^idc/$', views.idc, name='idc'),
    url(r'^new_idc/$', views.new_idc, name='new_idc'),
    url(r'^edit_idc/(?P<idc_id>\d+)/$', views.edit_idc, name='edit_idc'),
    url(r'^hostlist/(?P<idc_id>\d+)$', views.hostlist, name='hostlist'),
    url(r'^add_host/(?P<idc_id>\d+)$', views.add_host, name='add_host'),
    url(r'^edit_host/(?P<host_id>\d+)$', views.edit_host, name='edit_host'),
    url(r'^deploy/', views.deploy, name='deploy'),
    url(r'^packs/', views.packs, name='packs'),
    url(r'^uploads/', views.uploads, name='uploads'),
    url(r'^deploys/', views.deploys, name='deploys'),
    url(r'^upload_file/', views.upload_file, name='upload_file'),
    url(r'^rollback/', views.rollback, name='rollback'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
