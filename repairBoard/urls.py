from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'repairBoard.views.index', name='index'),
    url(r'^gallery$', 'repairBoard.views.gallery', name='gallery'),
    
    # url(r'^repairBoard/', include('repairBoard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include('adminBoard.urls', namespace="admin")),
    url(r'^summernote/', include('django_summernote.urls')),
)
