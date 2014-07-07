from django.conf.urls import patterns, include, url
from adminBoard import views

urlpatterns = patterns('adminBoard',
    url(r'^$','views.login',name='login'),
    url(r'^logout/','views.logout',name='logout'),
    url(r'^index$',views.index,name='index'),
    url(r'^company/(?P<pk>[^/]+)/update$', views.company_update, name='company_update'),
    url(r'^company/(?P<pk>[^/]+)/view$', views.company_detail, name='company_view'),
    url(r'^company/index$', views.company_index, name='company_index'),
    url(r'^company/contact$', views.company_contact, name='company_contact'),
    
    url(r'^appliance/index$', views.appliance_index_orig, name='appliance_index_orig'),
    url(r'^appliance/(?P<pk>[^/]+)/index$', views.appliance_index, name='appliance_index'),
    url(r'^appliance/(?P<pk>[^/]+)/create$', views.appliance_create, name='appliance_create'),
    url(r'^appliance/(?P<pk>[^/]+)/view$', views.appliance_view, name='appliance_view'),
    
    url(r'^appliance/(?P<pk>[^/]+)/(?P<appliance_id>[^/]+)/view$', views.appliance_single_view, name='appliance_single_view'),
    url(r'^appliance/(?P<pk>[^/]+)/(?P<appliance_id>[^/]+)/delete$', views.appliance_single_delete, name='appliance_single_delete'),
    url(r'^appliance/(?P<pk>[^/]+)/(?P<appliance_id>[^/]+)/update$', views.appliance_single_update, name='appliance_single_update'),
    
    url(r'^appliance_type/create$', views.appliance_type_create, name='appliance_type_create'),
    url(r'^appliance_type/(?P<type_id>[^/]+)/delete$', views.appliance_type_delete, name='appliance_type_delete'),
    #url(r'^appliance_type/(?P<type_id>[^/]+)/update$', views.appliance_type_update, name='appliance_type_update'),
)
