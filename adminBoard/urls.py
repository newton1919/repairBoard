from django.conf.urls import patterns, include, url
from adminBoard import views

urlpatterns = patterns('adminBoard',
    url(r'^$','views.login',name='login'),
    url(r'^logout/','views.logout',name='logout'),
    url(r'^index$',views.IndexView.as_view(),name='index'),
    url(r'^company/(?P<pk>[^/]+)/update$', views.company_update, name='company_update'),
    url(r'^company/(?P<pk>[^/]+)/detail$', views.company_detail, name='company_detail'),
)
