from django.test import TestCase
from channels.test import ChannelTestCase

from .consumers import PlayerConsumer

class PlayerConsumerTest(ChannelTestCase):
    
    def consumer_recieving messages
