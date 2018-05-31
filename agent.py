import random
from game import Game


class Agent:
    def __init__(self):
        pass

    def play(self, cards_played, cards_you_have, heart_broken, game_history):
        pass

    def pass_cards(self, cards):
        pass


class AgentRandom(Agent):
    def play(self, cards_played, cards_you_have, heart_broken, game_history):
        cards = Game.get_legal_moves(cards_played, cards_you_have, heart_broken)
        return random.choice(cards)

    def pass_cards(self, cards):
        return random.sample(cards, 3)


class MyAgent(Agent):
    '''
    You have to decide which card to play in this round
    gameknowlede is dictionary
    with keys: legalmoves, gamehistory, cards_left, turn
    legalmoves : a list object contain cards you can play 
    gamehistory : the cards your enemy and you have played in the past
    cards_left : a list object contain cards left in your hand
    turn : in range(0,3) 0 is the first to play in this round, 3 is the last.
    '''
    def play(self, cards_played, cards_you_have, heart_broken, game_history):
        return ...

    '''
    decide which three cards you want to give, the cards will be given to the guy who plays next
    0->1, 1->2, 2->3, 3->0

    cards : list of cards in your hand
    '''
    def pass_cards(self, cards):
        return ...
