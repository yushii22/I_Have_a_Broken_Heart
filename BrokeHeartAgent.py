import random


'''

'''
class easy_agent(object):
    def __init__(self):
        pass
    
    def playcard(self,gameknowledge):
        return random.choice(gameknowledge["legalmoves"])
    
    def changecard(self,cards):
        return random.sample(cards,3)
    

def your_agent(object):
    def __init__(self):
        pass
    
    '''
    You have to decide which card to play in this round
    
    gameknowlede is dictionary
    
    with keys: legalmoves, gamehistory, cards_left, turn
    legalmoves : a list object contain cards you can play 
    gamehistory : the cards your enemy and you have played in the past
    cards_left : a list object contain cards left in your hand
    turn : in range(0,3) 0 is the first to play in this round, 3 is the last.
    '''
    def playcard(self,gameknowledge):
        return random.choice(gameknowledge["legalmoves"])
    '''
    decide which three cards you want to give, the cards will be given to the guy who plays next
    0->1, 1->2, 2->3, 3->0
    
    cards : list of cards in your hand
    '''
    def changecard(self,cards):
        return random.sample(cards,3)
    

#define your teammates and your agent

#this is an example
MyAgents = [easy_agent() for i in range(4)]