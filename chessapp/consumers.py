import os

from channels import layers
from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Game

from chess import (Board, Move,
        A1, B1, C1, D1, E1, F1, G1, H1,
        A2, B2, C2, D2, E2, F2, G2, H2,
        A3, B3, C3, D3, E3, F3, G3, H3,
        A4, B4, C4, D4, E4, F4, G4, H4,
        A5, B5, C5, D5, E5, F5, G5, H5,
        A6, B6, C6, D6, E6, F6, G6, H6,
        A7, B7, C7, D7, E7, F7, G7, H7,
        A8, B8, C8, D8, E8, F8, G8, H8,)
from chess.svg import board as boardify
from asgiref.sync import sync_to_async

class PlayerConsumer(JsonWebsocketConsumer):

    def connect(self):
        # Setting variables from database
        self.setvalsdb()
        # Setting global "flipped" variable
        # For wether the board is flipped or not from user perspective
        # also doubles as another layer of authentication
        self.flipped = self.get_flipped()
        if self.flipped is None:
            self.close()
            return
        # Connecting to correct game layer
        self.channel_layer.group_add('gameid-'+self.gameid, self.channel_name)
        self.groups = ['gameid'+self.gameid]
        # Accept connection
        self.accept()

    def setvalsdb(self):
        # Setting value as global, since we're here anyways
        self.gameid = str(self.scope['url_route']['kwargs']['game_id'])
        # Fetching game from database
        self.game = Game.objects.get(pk=self.gameid)
        self.board = eval(self.game.board)
        self.board.move_stack = eval(self.game.moves)
        # Fetching user from database
        uid = self.scope['session']['_auth_user_id']
        self.user = User.objects.get(pk=uid)

    def get_flipped(self):
        username = self.user.username
        # Check if player is on white side
        if username == self.game.white:
            return False
        # Otherwise, check if player is on black side
        elif username == self.game.black:
            return True
        # If neither, the "player" is probably an impostor
        # That is how this also doubles as an extra layer of auth
        else:
            return None

    def move(self, mv):
        try:
            self.board.push_uci(mv)
        except:
            pass
        self.game.board = repr(self.board)
        self.game.moves = repr(self.board.move_stack)
        self.game.save()
        return boardify(self.board, lastmove=self.get_movestack(), flipped=self.flipped)

    def get_movestack(self):
        try: mv = self.board.move_stack[-1]
        except: mv = None
        return mv

    def initial_validate_move(self, mv):
        piece = str(self.board.piece_at(eval(mv[:2].upper())))
        upper = (piece == piece.upper())
        if upper ^ self.flipped:
            print(True)
            return True
        return False

    def receive_json(self, data):
        t = data['type']
        if t == 'HEARTBEAT':
            self.send_json({'type':'HEARTBEAT'})
        if t == 'MOVE':
            mv = data['data']
            validated = self.initial_validate_move(mv)
            if validated == False:
                return
            new_board = self.move(mv)
            data = {'type':'MOVEPROCESSED', 'data':new_board}
            self.send_json(data)
            self.channel_layer.group_send('serverside.move', data)

    def serverside_move(self, data):
        print('Got this!')
        self.send_json(data)

    def disconnect(self, close_code):
        self.channel_layer.group_discard('gameid-'+self.gameid, self.channel_name)

class AsyncPlayerConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # Setting variables from database
        await database_sync_to_async(self.setvalsdb)()
        # Setting global "flipped" variable
        # For whether the board is flipped or not from user perspective
        # Also doubles as another layer of authentication
        self.flipped = await self.get_flipped()
        if self.flipped is None:
            await self.close()
            return
        # Connecting to correct game layer
        await self.channel_layer.group_add('gameid-'+self.gameid, self.channel_name)
        # Accept connection
        await self.accept()

    def setvalsdb(self):
        # Setting value as global, since we're here anyways
        self.gameid = str(self.scope['url_route']['kwargs']['game_id'])
        # Fetching game from database
        self.game = Game.objects.get(pk=self.gameid)
        self.board = eval(self.game.board)
        # Fetching user from database
        uid = self.scope['session']['_auth_user_id']
        self.user = User.objects.get(pk=uid)

    async def get_flipped(self):
        username = self.user.username
        # Check if player is on white side
        if username == self.game.white:
            return False
        # Otherwise, check if player is on black side
        elif username == self.game.black:
            return True
        # If neither, the "player" is probably an impostor
        # That is how this also doubles as an extra layer of auth
        else:
            return None

    async def move(self, mv):
        await sync_to_async(self.board.push_uci)(mv)
        self.game.board = repr(self.board)
        await database_sync_to_async(self.save_game)()
        return boardify(b, lastmove=b.move_stack[-1], flipped=self.flipped)

    def save_game(self):
        self.game.save()

    async def receive_json(self, data):
        t = data['type']
        if t == 'HEARTBEAT':
            await self.send_json({'type':'HEARTBEAT'})
        if t == 'MOVE':
            new_board = await self.move(data['data'])
            print(new_board)
            data = {'type':'MOVEPROCESSED', 'data':new_board}
            await self.send_json(data)
            await self.channel_layer.group_send('serverside.move', data)

    async def serverside_move(self, data):
        await self.send_json(data)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('gameid-'+self.gameid, self.channel_name)


