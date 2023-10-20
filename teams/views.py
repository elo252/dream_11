from django.shortcuts import render,redirect
from django.http import HttpResponse,  response
from. models import *


from .models import Team,Player 
from .serializers import PlayerSerializer , TeamSerializer
from rest_framework import generics
from .forms import TeamForm,PlayerForm

from .helper import combinations_creator,create_df, input_players,create_df_input,fixed_structure , unfixed_structure


# Create your views here.
def home(request):
    return render(request, "index.html",)

def upd_player(request,pk , team_id):
    player = Player.objects.get(id=pk)
    form = PlayerForm(instance=player)
    team = Team.objects.get(id=team_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
    context = {"form":form , "team":team}
    return render(request ,"update_player.html",context)

def del_player(request,pk, team_id):
    player = Player.objects.get(id=pk)
    team = Team.objects.get(id =team_id)
    context= {"player":player,"team":team}
    if request.method == "POST":
        option = request.POST.get('option') 
        if option == "yes": 
            if team in player.teams.all():
                player.teams.remove(team)
                player.save()
                team.players.remove(player)
                team.save()
    return render(request ,"delete_player.html",context)

def delete_players(request,id):
    queryset= Player.objects.get(id=id)
    queryset.delete()
    return redirect('teams')

def delete_player(request,pk):
    print(pk)
    return HttpResponse("Hi")
    return render(request , "delete_player.html",)




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


def udpate_team(request,pk):
    #print(pk)
    team = Team.objects.get(id=pk)
    players = team.players.all()
    teamform = TeamForm(instance = team)
    if request.method == "POST":
        if request.POST.get('name'):
            team.name = request.POST.get('name')
            team.save()

    context = {"teamform":teamform, "players":players, "team":team }
    return render(request , "update.html" ,context)

def update_player(request,pk):
    pass 

def delete_player(request,pk):
    pass 




def matchday(request):
    teams = Team.objects.all()
    context={"teams" : teams }
    if request.method=="POST":
        selected_team_id_1 = request.POST['team1']
        selected_team_1 = Team.objects.get(id=selected_team_id_1)
        players_list1= selected_team_1.players.all()
        selected_team_id_2 = request.POST['team2']
        selected_team_2 = Team.objects.get(id=selected_team_id_2)
        players_list2 = selected_team_2.players.all()
        algo_teams_df =create_df(players_list1,players_list2)
        algo_teams = fixed_structure(algo_teams_df)
        combined_players=list(players_list1)+ list(players_list2)
        pair1 = combinations_creator(players_list1,algo_teams) 
        pair2 = combinations_creator(players_list2,algo_teams)
        #pair3 = combinations_creator(combined_players,algo_teams)
        #input_team = input_players()haa

        context={"teams":teams , "pair1": pair1 , "pair2": pair2 ,"team1":selected_team_1 , "team2": selected_team_2 ,  "algo_teams":algo_teams} 

        return render(request, 'match.html', context)

    return render(request, 'match.html', context)

def matchday_Input(request):
    teams = Team.objects.all()
    context={"teams" : teams }
    players=Player.objects.all()
    context['players']=players
    if request.method=="POST":
        selected_team_id_1 = request.POST['team1']
        selected_team_1 = Team.objects.get(id=selected_team_id_1)
        players_list1= selected_team_1.players.all()
        selected_team_id_2 = request.POST['team2']
        selected_team_2 = Team.objects.get(id=selected_team_id_2)
        players_list2 = selected_team_2.players.all()
        batsman = int(request.POST['batsman'])
        bowler = int(request.POST['bowler'])
        wk = int(request.POST['wicketKeeper'])
        alrou = int(request.POST['allRounder'])
        algo_teams_input =create_df_input(players_list1,players_list2,batsman,bowler,wk,alrou)


        context={"teams":teams ,"team1":selected_team_1 , "team2": selected_team_2 ,  "algo_teams_input":algo_teams_input} 

        return render(request, 'matchday_input.html', context)

    return render(request, 'matchday_input.html', context)



def unfixed(request):
    teams=Team.objects.all()
    context={"teams":teams}
    if request.method=="POST":
        team1 =request.POST['team1']
        selected_team_1 = Team.objects.get(id=team1)
        players_list1= selected_team_1.players.all()
        team2=request.POST['team2']
        selected_team_id_2 = request.POST['team2']
        selected_team_2 = Team.objects.get(id=selected_team_id_2)
        players_list2 = selected_team_2.players.all()
        algo_df = create_df(players_list1,players_list2)
        algo_teams = unfixed_structure(algo_df)
        context ={"teams":teams , "algo_teams": algo_teams }
        return render(request,'unfixed.html',context)
    return render(request,'unfixed.html',context)