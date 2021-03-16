from django.urls import path

from . import views, consumers

app_name = 'chessapp'
urlpatterns = [
               path('', views.login, name='login'), # User side
               path('play-<int:game_id>', views.game, name='game'), # User side
               path('home', views.home, name='home'), # User side
    	       path('create', views.create, name='create'), # Server side
               path('new', views.new, name='new'), # User side
	           path('submit', views.submit, name='submit'), # Server side
	          ]
