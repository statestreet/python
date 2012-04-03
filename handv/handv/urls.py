from django.conf.urls.defaults import *
from handv.home.home import *
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',  home),  
    (r'^article/(\w+)/$', article),
    (r'^articles/', articles),
    (r'^photos/', photos),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"]) + '/html/css'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"]) + '/html/images'}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"]) + '/html/js'}),
      
    # Example:
    # (r'^handv/', include('handv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
