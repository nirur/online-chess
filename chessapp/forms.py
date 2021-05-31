from django.forms import *


class LoginForm(Form):
    username = CharField(label="Username", required=True)
    password = CharField(label="Password", widget=PasswordInput, required=True)


class NewgameForm(Form):
    CHOICES_SIDE = [('white', 'white'),
                    ('black', 'black')]
    opposition = ChoiceField(choices=[], widget=RadioSelect, required=True)
    side = ChoiceField(choices=CHOICES_SIDE, widget=RadioSelect, required=True)
    name = CharField(required=True)
