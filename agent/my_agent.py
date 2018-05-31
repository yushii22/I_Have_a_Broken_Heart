# -*- coding: utf-8 -*-
from agent import Agent


class MyAgent(Agent):
    '''
    You have to decide which card to play in this round.
    cards_played: cards that has been played this round
    cards_you_have: list of cards in your hand
    heart_broken: heart is broken or not
    history: cards played in previous rounds
    '''
    def play(self, cards_played, cards_you_have, heart_broken, info):
        return ...

    '''
    decide cards you want to pass to the player next to you
    0->1, 1->2, 2->3, 3->0

    cards: list of cards in your hand
    '''
    def pass_cards(self, cards):
        return ...
