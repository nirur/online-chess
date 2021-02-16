from django.forms import *

class LoginForm(Form):
    username = CharField(label="Username")
    password = CharField(label="Password", widget=PasswordInput)

class NewgameForm(Form):
    CHOICES_SIDE = [('white', 'white'),
                   ('black', 'black')]
    opposition = ChoiceField(choices=[], widget=RadioSelect, required=True)
    side = ChoiceField(choices=CHOICES_SIDE, widget=RadioSelect, required=True)
    name = CharField(required=True)
