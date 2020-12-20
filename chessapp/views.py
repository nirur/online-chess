from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User

from chess import svg, Board, Move

from .models import Game

def game(request, game_id, side):
	print(dir(request))
	try:
		game = Game.objects.get(pk=game_id)
	except Game.DoesNotExist:
		return Http404()
	if side == 'white':
		flipped = False
	elif side == 'black':
		flipped = True
	try:
		lastmove=eval(game.moves[-1])
	except IndexError:
		lastmove = None
	gameboard = svg.board(
		game.board,
		flipped=flipped,
		lastmove = eval(game.moves)[-1]
		)
	context = {'game':game, 'current_board':gameboard}
	return render(request, 'chessapp/play.html', context)

def home(request):
	#user = User.objects.get(username=request.COOKIES['username'])
	#players = []
	#for group in user.groups.all():
	#	for player in group.user_set.all():
	#		if player is user:
	#			continue
	#		if player is not user:
	#			players.append(player)
	#context_players = {'players':players}
	#games_white = []
	#games_black = []
	#for g in Game.objects.all():
	#	if g.white == user.username and not g.finished:
	#		games_white.append(g)
	#	elif g.black == user.username and not g.finished:
	#		games_black.append(g)
	#if len(games_white+games_black) != 0:
	#	context_games = {'games_white':games_white[::-1], 'games_black':games_black[::-1],\
        #           'heading':'Your games'}
	#else:
	#	context_games = {'games_white':'', 'games_black':'',\
        #           'heading':'No games'}
	#context = {**context_games, **context_players}
	context = {}
	return render(request, 'chessapp/home.html', context)

def validate(uname, passwrd):
    try:
        user = User.objects.get(username=uname)
        assert user.check_password(passwrd)
        return True
    except (AssertionError, User.DoesNotExist):
        return False

def submit(request):
    output = validate(request.POST['username'], request.POST['password'])
    if output is True:
        context = {'uname':request.POST['username']}
        return render(request, "chessapp/submit.html", context)
    else:
        return HttpResponseRedirect('../?invalid=True')

def login(request):
    print(request.META["REMOTE_ADDR"])
    context = {'invalid_login':''}
    try:
        if request.GET['invalid'] == 'True':
            context = {'invalid_login':'Invalid username or password'}
        elif request.GET['empty'] == 'True':
            context['invalid_login'] = "You need to type something in both spots"
        else:
            pass
    except:
        pass
    return render(request, 'chessapp/login.html', context)

def create(request):
    request.POST['opposition']

def new(request):
    context = {'opponent':request.GET['o']}
    return render(request, 'chessapp/create.html', context)

def err404(request, exception):
    context = {}
    return render(request, 'chessapp/error_404.html', context)

def err500(request):
    context = {}
    return render(request, 'chessapp/error_500.html', context)

