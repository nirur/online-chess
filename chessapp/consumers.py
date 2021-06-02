import os

from channels import layers
from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Game

import chess
from chess import Board, Move, SquareSet
from chess.svg import board as boardify
from asgiref.sync import sync_to_async, async_to_sync


class PlayerConsumer(JsonWebsocketConsumer):

    def connect(self):
        # Setting variables from database
        self.setvalsdb()
        # Setting global "flipped" variable
        # For whether the board is flipped or not from user perspective
        # also doubles as another layer of authentication
        self.flipped = self.get_flipped()
        if self.flipped is None:
            self.close()
            return
        # Connecting to correct game layer
        async_to_sync(self.channel_layer.group_add)('gameid-' + self.gameid, self.channel_name)
        # Accept connection
        self.accept()
        # For video connection
        self.addr = ':'.join([str(itm) for itm in self.scope['client']])

    def setvalsdb(self):
        # Setting value as global, since we're here anyways
        self.gameid = str(self.scope['url_route']['kwargs']['game_id'])
        # Fetching game from database
        self.game = Game.objects.get(pk=self.gameid)
        self.board = eval(self.game.board)
        self.board.move_stack = [Move.from_uci(itm) for itm in eval(self.game.moves)]
        # Fetching user from database
        uid = self.scope['session']['_auth_user_id']
        self.user = User.objects.get(pk=uid)

    def get_flipped(self):
        username = self.user.username
        # Check if player is on white side
        if username == self.game.white:
            return True
        # Otherwise, check if player is on black side
        elif username == self.game.black:
            return False
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
        self.game.moves = repr([str(itm) for itm in self.board.move_stack])
        self.game.save()
        checks = self.get_checks()
        checked_square = None
        if checks[0] == 'not over':
            if checks[1] == 'check':
                checked_square = checks[2]
        elif checks[0] == 'game over':
            self.send_json(
                {
                    'type': 'GAMEOVER',
                    'data': [checks[1], boardify(
                        self.board, lastmove=self.get_movestack(), orientation=self.flipped, check=checks[2]
                    )
                             ]
                }
            )
            self.game.status = checks[1]
            self.game.save()
            return None
        return boardify(
            self.board, lastmove=self.get_movestack(), orientation=self.flipped, check=checked_square
        )

    def get_movestack(self):
        try:
            mv = self.board.move_stack[-1]
        except:
            mv = None
        return mv

    def initial_validate_move(self, mv):
        if len(mv) < 3:
            first_two = mv
        else:
            first_two = mv[:2]
        piece = str(self.board.piece_at(getattr(chess, first_two.upper())))
        upper = (piece == piece.upper())
        if upper == self.flipped:
            return True
        return False

    def get_checks(self):
        gameover = self.board.is_game_over()
        if not gameover and self.board.is_check():
            return 'not over', 'check', self.board.king(self.board.turn)
        elif gameover:
            # Check for checkmates
            checkmate = self.board.is_checkmate()
            # Check for a draw of any type
            stalemate = self.board.is_stalemate()
            insufficient_material = self.board.is_insufficient_material()
            seventyfive_moves = self.board.is_seventyfive_moves()
            fivefold_repetition = self.board.is_fivefold_repetition()
            # Summarize the condition for a draw
            draw = (stalemate or insufficient_material or seventyfive_moves or fivefold_repetition)
            # Now run the checks
            if checkmate:
                if self.board.turn:
                    winner = 'black'
                elif not self.board.turn:
                    winner = 'white'
                return 'game over', f'Checkmate - {winner} wins', self.board.king(self.board.turn)
            elif draw:
                if stalemate:
                    reason = 'Stalemate'
                elif insufficient_material:
                    reason = 'Insufficient material for either side to win'
                elif seventyfive_moves:
                    reason = '75 move limit reached'
                elif fivefold_repetition:
                    reason = 'Same position repeated 5 times'
                return 'game over', 'Draw', f'It\'s a draw!\n{reason}'
        return 'not over', None

    def receive_json(self, data):
        t = data['type']
        if t == 'HEARTBEAT':
            self.send_json({'type': 'HEARTBEAT'})
        elif t == 'STREAM':
            self.stream = data['data']
            self.stream_init()
        elif t == 'POSTGAME':
            if data['data'] == 'delete':
                self.game.delete()
            return
        elif t == 'PIECECLICK':
            validate = self.initial_validate_move(data['data'])
            if not validate:
                return
            possiblemoves = []
            for legalmove in self.board.legal_moves:
                if str(legalmove).startswith(data['data']):
                    possiblemoves.append(str(legalmove))
            possiblemoves = SquareSet([getattr(chess, mv[2:].upper()) for mv in possiblemoves])
            b = boardify(self.board, orientation=self.flipped, squares=possiblemoves)
            self.send_json({'type': 'PROCESSED', 'data': b})
        elif t == 'MOVE':
            mv = data['data']
            validated = self.initial_validate_move(mv)
            if validated == False:
                return
            new_board = self.move(mv)
            if new_board is None:
                return
            data = {'type': 'PROCESSED', 'data': new_board}
            self.send_json(data)
            serverdata = {'type': 'move.serverside',
                          'data': ([str(itm) for itm in self.board.move_stack], repr(self.board))}
            async_to_sync(self.channel_layer.group_send)('gameid-' + self.gameid, serverdata)

    def move_serverside(self, data):
        self.board = eval(data['data'][1])
        self.board.move_stack = [Move.from_uci(itm) for itm in data['data'][0]]
        self.game.board = repr(self.board)
        self.game.moves = repr(data['data'][0])
        self.game.save()
        b = boardify(self.board, orientation=self.flipped, lastmove=self.get_movestack())
        self.send_json({'type': 'PROCESSED', 'data': b})

    def stream_init(self):
        async_to_sync(self.channel_layer.group_send)('gameid-' + self.gameid,
                                                     {'type': 'receive.stream', 'data': [self.stream, True]})

    def receive_stream(self, data):
        self.send_json({'type': 'STREAM', 'data': data['data'][0]})
        if data['data'][1]:
            async_to_sync(self.channel_layer.group_send)('gameid-' + self.gameid,
                                                         {'type': 'receive.stream', 'data': [self.stream, False]})

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('gameid-' + self.gameid, self.channel_name)
