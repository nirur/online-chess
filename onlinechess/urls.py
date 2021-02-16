from django.contrib import admin
from django.urls import *
from django.conf.urls.static import serve
from django.conf import settings

from chessapp.views import err404, err500

urlpatterns = [
			path('', include('chessapp.urls'), name='chessapp'),
            path('staff', admin.site.urls, name='staff'),
			]
handler404 = err404
handler500 = err500
