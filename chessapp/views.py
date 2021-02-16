from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate, get_user

from chess import svg, Board, Move

from .models import Game
from .forms import *


def get_choices(user):
    '''Server-only opponent finding function'''
    opponents = []
    for group in user.groups.all():
        for opponent in group.user_set.all():
            if (opponent is not user) and (opponent not in opponents):
                opponents.append(opponent)
    opponents = [(opponent.username, opponent.username) for opponent in opponents]
    opponents += [('NiraoAdmin641', 'NiraoAdmin641'), ('Guest1', 'Guest1')]
    return opponents

def login(request):
    '''User-side login page'''
    invalid_login=''
    if 'invalid' in request.GET.keys():
        invalid_login="Invalid username or password"
    context = {'invalid_login':invalid_login, 'form':LoginForm()}
    return render(request, 'chessapp/login.html', context)

def submit(request):
    '''Server-side login function'''
    form = LoginForm(request.POST)
    try:
        assert form.is_valid()
        data = form.cleaned_data
        usr = auth_authenticate(request, username=data['username'], password=data['password'])
        assert usr is not None
        auth_login(request, usr)
        return HttpResponsePermanentRedirect('../home')
    except AssertionError:
        return HttpResponseRedirect('../?invalid=')

def game(request, game_id):
    '''User-side game page'''
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return HttpResponseRedirect('../home?err=')
    player = get_user(request)
    if game.white == player.username:
        flipped = False
    elif game.black == player.username:
        flipped = True
    try:
        lastmove=eval(game.moves)[-1]
    except IndexError:
        lastmove = None
    gameboard = svg.board(eval(game.board), flipped=flipped, lastmove=lastmove)
    context = {'game':game, 'current_board':gameboard}
    return render(request, 'chessapp/play.html', context)

def client_move(request, game_id):
    '''Server-side game 'client made a move' request handler'''
    pass

def page_update(request, game_id):
    '''Server-side game page continuous updating request handler'''
    pass

def home(request):
    '''User-side homepage'''
    context_alerts = {"alerts":[]}
    if 'sent' in request.GET.keys():
        context_alerts['alerts'].append('Request Successfuly Sent!')
    if 'err' in request.GET.keys():
        context_alerts['alerts'].append('Sorry, an error occured')
    try:
        user = get_user(request)
    except IndexError:
        return HttpResponseRedirect("../?invalid=")
    games_white = []
    games_black = []
    for g in Game.objects.all():
        if g.white == user.username and not g.status.startswith('finished'):
            games_white.append(g)
        elif g.black == user.username and not g.status.startswith('finished'):
            games_black.append(g)
    if len(games_white+games_black) != 0:
        context_games = {'games_white':games_white[::-1], 'games_black':games_black[::-1], 'no_games':''}
    else:
        context_games = {'games_white':'', 'games_black':'', 'no_games':'No games currently. Check back later or start a new one now.'}
    context = {**context_games, **context_alerts}
    return render(request, 'chessapp/home.html', context)

def create(request):
    '''Server-side "New Game" page'''
    try:
        user = get_user(request)
    except:
        return HttpResponseRedirect('../')
    form = NewgameForm(request.POST)
    form.fields['opposition']._set_choices(get_choices(user))
    if not form.is_valid():
        return HttpResponseRedirect('../home?err=')
    data = form.cleaned_data
    if data['side'] == "white":
        args = {'white':user.username, 'black':request.POST['opposition']}
    elif data['side'] == "black":
        args = {'white':request.POST['opposition'], 'black':user.username}
    args['name'] = data['name']
    game = Game(**args)
    game.save()
    return HttpResponseRedirect('../home?sent=')

def new(request):
    '''User-side "New Game" function'''
    try:
        user = get_user(request)
    except:
        return HttpResponseRedirect('../?invalid=')
    form = NewgameForm()
    form.fields['opposition']._set_choices(get_choices(user))
    context = {'form':form}
    return render(request, 'chessapp/new.html', context)

def err404(request, exception):
    '''404 page'''
    context = {}
    return render(request, 'chessapp/error_404.html', context)

def err500(request):
    '''500(internal server error) page'''
    context = {}
    return render(request, 'chessapp/error_500.html', context)

