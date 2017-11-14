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
    #url(r'^host/$', views.host, name='host'),
    url(r'^(\d+)$', views.host, name='host'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
