from django.db.models import *

from chess import Board

class Game(Model):
    finished = False
    status = 'in progress'
    name = CharField(max_length=10, default="")
    white = CharField(max_length=20, default="")
    black = CharField(max_length=20, default="")
    board = CharField(max_length=40, default='Board()')
    moves = CharField(max_length=3000, default='[]')
    
    def __str__(self):
        return "[%s]: %s vs %s" % (self.name, self.white, self.black)
    
    def update_endgame(self, status, save_game):
        self.finished = True
        self.status = status
        if not save_game:
            self.delete()
