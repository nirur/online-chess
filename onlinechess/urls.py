from django.contrib import admin
from django.urls import *
from django.conf.urls.static import serve
from django.conf import settings

from chessapp.views import err404, err500

urlpatterns = [path('', include('chessapp.urls')),
            path('staff', admin.site.urls, name='staff'),
            #re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
			#re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
			]
handler404 = err404
handler500 = err500
