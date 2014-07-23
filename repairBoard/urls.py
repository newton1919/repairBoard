from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'repairBoard.views.index', name='index'),
    url(r'^company/index$', 'repairBoard.views.index', name='index2'),
    url(r'^company/contact$', "repairBoard.views.company_contact", name='company_contact'),
    url(r'^gallery$', 'repairBoard.views.gallery', name='gallery'),
    
    # url(r'^repairBoard/', include('repairBoard.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include('adminBoard.urls', namespace="admin")),
    url(r'^summernote/', include('django_summernote.urls')),
    
    url(r'^appliance/(?P<pk>[^/]+)/index$', "repairBoard.views.appliance_index", name='appliance_index'),
    url(r'^appliance/(?P<pk>[^/]+)/(?P<appliance_id>[^/]+)/view$', "repairBoard.views.appliance_single_view", name='appliance_single_view'),    
    
    url(r'^language$', "repairBoard.views.language"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
)
