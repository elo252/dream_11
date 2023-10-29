from django.contrib import admin
from django.urls import path,include 
from .views import *


urlpatterns = [
    path('players_list/', PlayerList.as_view(), name='players_list'),
    path('update_player/' , PlayerDetail.as_view(),name = 'update_player'),
    path('team_list/',  TeamList.as_view()),
    path('update_team/', TeamDetail.as_view()),
    path('team/', create_team, name='create_team'),
    path('player/', create_player, name='create_player'),
    path('match/',matchday, name='match'),
    path('matchday_input/',matchday_Input, name='matchday_input'),
    path('unfixed/',unfixed,name="unfixed"),
    path('updateteam/<int:pk>',udpate_team,name="update"),
    path('updateplayer/<int:pk>/<team_id>/',upd_player,name="update_player"),
    path('deleteplayer/<int:pk>/<team_id>/',del_player,name="delete_player"),
    path('add_player_team/<int:id>',add_player_team,name="add")
]