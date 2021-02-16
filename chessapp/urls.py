from django.urls import path

from . import views, consumers

app_name = 'chessapp'
urlpatterns = [
               path('', views.login, name='login'),
               path('play-<int:game_id>', views.game, name='game'),
               path('home', views.home, name='home'),
    	       path('create', views.create, name='create'),
               path('new', views.new, name='new'),
	           path('submit', views.submit, name='submit'),
	          ]
