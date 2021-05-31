from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate, get_user

from chess import svg, Board, Move

from .models import Game, Request
from .forms import *


def get_choices(user):
    """Server-only opponent finding function"""
    opponents = []
    for group in user.groups.all():
        for opponent in group.user_set.all():
            if (opponent.username != user.username) and (opponent.username not in opponents):
                opponents.append(opponent.username)
    opponents = [(opponent, opponent) for opponent in opponents]
    opponents += [('NiraoAdmin641', 'NiraoAdmin641'), ('Guest1', 'Guest1')]
    return opponents


def login(request):
    """User-side login page"""
    invalid_login = ''
    if 'invalid' in request.GET.keys():
        invalid_login = "Invalid username or password"
    context = {'invalid_login': invalid_login, 'form': LoginForm()}
    return render(request, 'chessapp/login.html', context)


def submit(request):
    """Server-side login function"""
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
    """User-side game page"""
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
        lastmove = Move.from_uci(eval(game.moves)[-1])
    except IndexError:
        lastmove = None
    gameboard = svg.board(eval(game.board), flipped=flipped, lastmove=lastmove)
    context = {'game': game, 'current_board': gameboard}
    return render(request, 'chessapp/play.html', context)


def home(request):
    """User-side homepage"""
    context_alerts = {"alerts": []}
    if 'sent' in request.GET.keys():
        context_alerts['alerts'].append('Request Successfully Sent!')
    if 'err' in request.GET.keys():
        context_alerts['alerts'].append('Sorry, an error occurred')
    try:
        user = get_user(request)
    except IndexError:
        return HttpResponseRedirect("../?invalid=")
    main_white = []
    main_black = []
    boards_white = []
    boards_black = []
    for g in Game.objects.all():
        if g.white == user.username and not g.status.startswith('finished'):
            main_white.append(g)
            boards_white.append(svg.board(eval(g.board)))
        elif g.black == user.username and not g.status.startswith('finished'):
            main_black.append(g)
            boards_black.append(svg.board(eval(g.board)))
    if len(main_white + main_black) != 0:
        games_white = []
        for itm in zip(main_white, boards_white):
            games_white.append(itm)
        games_black = []
        for itm in zip(main_black, boards_black):
            games_black.append(itm)
        context_games = {
            'games_white': reversed(games_white), 'games_black': reversed(games_black), 'no_games': ''
        }
    else:
        context_games = {'games_white': '', 'games_black': '',
                         'no_games': 'No games currently.'}
    reqs_ids = []
    reqs_senders = []
    reqs_names = []
    for r in Request.objects.all():
        if r.receiver == user.username:
            print("hi")
            reqs_ids.append(id(r))
            reqs_senders.append(r.sender)
            reqs_names.append(r.name)
    reqs = [itm for itm in zip(reqs_ids, reqs_names, reqs_senders)]
    print(reqs)
    context = {**context_games, **context_alerts, "requests": reqs}
    return render(request, 'chessapp/home.html', context)


def create(request):
    """Server-side "New Game" page"""
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
        args = {'white': user.username, 'black': request.POST['opposition']}
    elif data['side'] == "black":
        args = {'white': request.POST['opposition'], 'black': user.username}
    args['name'] = data['name']
    args['sender'] = user.username
    args['receiver'] = request.POST['opposition']
    req = Request(**args)
    req.save()
    return HttpResponseRedirect('../home?sent=')


def new(request):
    """User-side "New Game" function"""
    try:
        user = get_user(request)
    except:
        return HttpResponseRedirect('../?invalid=')
    form = NewgameForm()
    form.fields['opposition']._set_choices(get_choices(user))
    context = {'form': form}
    return render(request, 'chessapp/new.html', context)


def accept(request):
    """Server-side "accept a request" function"""
    req = Request.objects.get(pk=request.POST['id'])
    g = Game(name=req.name, white=req.white, black=req.black)
    g.save()


def err404(request, exception):
    """404 page"""
    context = {}
    return render(request, 'chessapp/error_404.html', context)


def err500(request):
    """500(internal server error) page"""
    context = {}
    return render(request, 'chessapp/error_500.html', context)
