from django.db.models import *

from chess import Board


class Game(Model):
    status = CharField(max_length=100, default='in progress')
    name = CharField(max_length=10, default="")
    white = CharField(max_length=30, default="")
    black = CharField(max_length=30, default="")
    board = CharField(max_length=100, default='Board()')
    moves = CharField(max_length=10000, default="[]")

    def __str__(self):
        return "[%s]: %s vs %s" % (self.name, self.white, self.black)

    def update_endgame(self, status, save_game):
        self.status = status
        if not save_game:
            self.delete()


class Request(Model):
    sender = CharField(max_length=100, default="")
    receiver = CharField(max_length=100, default="")
    white = CharField(max_length=30, default="")
    black = CharField(max_length=30, default="")
    name = CharField(max_length=100, default="")
