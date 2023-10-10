from django.shortcuts import render,redirect
from django.http import HttpResponse,  response
from. models import *


from .models import Team,Player 
from .serializers import PlayerSerializer , TeamSerializer
from rest_framework import generics
from .forms import TeamForm,PlayerForm

from .helper import combinations_creator,create_df


# Create your views here.
def teams(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        team = data.get('team')
        points = float(data.get('points', 0))  # Assuming points can be a float
        position = data.get('position')

        # Create a new Player instance using Player.objects.create()
        Player.objects.create(name=name, team=team, points=points, position=position)
        return redirect('teams')
    
    queryset = Player.objects.all()
    context = {'players': queryset}

    return render(request, "index.html", context)

def delete_players(request,id):
    queryset= Player.objects.get(id=id)
    queryset.delete()
    return redirect('teams')




class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer 


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer 

from rest_framework.generics import ListCreateAPIView
from .models import Team
from .serializers import TeamSerializer

class TeamList2(ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

def create_team(request):
    form=TeamForm()
    context= {"form":form}
        # Render the team.html template if the request is a GET request.
    teams=Team.objects.all()
    context['teams']=teams
        # Save the form data to the database if the request is a POST request.
    if request.method == 'POST':
        form=TeamForm(request.POST)
            #print(1)
        if form.is_valid():
            form.save()
                #print(2)
    return render(request, 'team.html',context)


def create_player(request):
    form=PlayerForm()
    #print(Team.objects.first())
    context= {"form":form}
        # Render the team.html template if the request is a GET request.
    players=Player.objects.all()
    context['players']=players
        # Save the form data to the database if the request is a POST request.
    if request.method == 'POST':
        form=PlayerForm(request.POST)

            #print(1)
        if form.is_valid():
            form.save()
            current_player = Player.objects.get(pk=form.instance.pk)
            print(form.cleaned_data['teams'])
            current_team=form.cleaned_data['teams']
            current_team[0].players.add(current_player)
                #print(2)
    return render(request, 'players.html',context) 


def udpate_team():
    pass




def matchday(request):
    teams = Team.objects.all()
    context={"teams" : teams }
    if request.method=="POST":
        selected_team_id_1 = request.POST['team1']
        selected_team_1 = Team.objects.get(id=selected_team_id_1)
        players_list1= selected_team_1.players.all()
        pair1 = combinations_creator(players_list1)
        selected_team_id_2 = request.POST['team2']
        selected_team_2 = Team.objects.get(id=selected_team_id_2)
        players_list2 = selected_team_2.players.all()
        pair2 = combinations_creator(players_list2)
        zz=create_df(players_list1,players_list2)
        print(zz)
        combined_players=list(players_list1)+ list(players_list2) 
        pair3 = combinations_creator(combined_players)
        context={"teams":teams , "pair1": pair1 , "pair2": pair2 ,"team1":selected_team_1 , "team2": selected_team_2 , "pair3": pair3} 

        return render(request, 'match.html', context)

    return render(request, 'match.html', context)
       