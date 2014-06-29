from django.conf.urls import patterns, include, url
from adminBoard import views

urlpatterns = patterns('adminBoard',
    url(r'^$','views.login',name='login'),
    url(r'^logout/','views.logout',name='logout'),
    url(r'^index$',views.index,name='index'),
    url(r'^company/(?P<pk>[^/]+)/update$', views.company_update, name='company_update'),
    url(r'^company/(?P<pk>[^/]+)/view$', views.company_detail, name='company_view'),
    url(r'^company/index$', views.company_index, name='company_index'),
)
