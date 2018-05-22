from enum import Enum
import random
from collections import defaultdict
import BrokeHeartAgent


class Colored(Enum):
    SPADE = "♠"
    HEART = "♥"
    DIAMOND = "♦"
    CLUB = "♣"
    
#each player has 13 cards
card_order =  [1,13,12,11,10,9,8,7,6,5,4,3,2]
card_color = [Colored.HEART,Colored.SPADE,Colored.DIAMOND,Colored.CLUB]
    
class Card(object):
    
    
    def __init__(self,color,number):
        self.color = color
        self.number = number
        
    def __str__(self):
        return self.color.value+str(self.number)
    def __repr__(self):
        return self.color.value+str(self.number)
    
    def __eq__(self,Other):
        
        if not isinstance(Other,Card):
            return False
        
        if self.color == Other.color and self.number == Other.number:
            return True
        return False
    
    def __hash__(self):
        return self.number + card_color.index(self.color)*13
    
pointcards = {Card(Colored.HEART,num):1 for num in  card_order}
pointcards[Card(Colored.SPADE,12)] = 13

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
def card_cmp(x,y):
    indexX = card_color.index(x.color)
    indexY = card_color.index(y.color)

    if indexX < indexY:
        return 1
    elif indexX > indexY:
        return -1
    else:
        indexX = card_order.index(x.number)
        indexY = card_order.index(y.number)

        if indexX < indexY:
            return 1
        elif indexX > indexY:
            return -1
        else:
            return 0

class player(object):

    # list of 13 cards
    def __init__(self,Cards):
        self.Cards = Cards
        self.order()
    def order(self):
        self.Cards = sorted(self.Cards,key=cmp_to_key(card_cmp))
    def playcard(self,card):
        self.Cards.remove(card)
        return 0

class Game(object):

    def __init__(self):
        self.set_game()

        
    def set_game(self):
        Poker = [Card(color,num) for num in  card_order for color in card_color]
        random.shuffle(Poker)
        self.Hand = [player(Poker[:13]),player(Poker[13:26]),player(Poker[26:39]),player(Poker[39:])]
        self.Agents = BrokeHeartAgent.MyAgents
        self.changecard([self.Agents[i].changecard(self.Hand[i].Cards[:]) for i in range(4)])
        self.turn = 0
        
        for i in range(3):
            if Card(Colored.CLUB,2) in self.Hand[i].Cards:
                break
            self.turn+=1
        self.currentType = None
        self.gamehistory = []
        
        self.round = 1
        self.breakheart = False
        self.score = [0 for _ in range(4)]
        self.gameknowledge = dict()
        self.gameknowledge["history"] = self.gamehistory
        print("Game Start")



    def rounds(self,idx):

        card_played = []
        self.gamehistory.append(card_played)

        for position in range(4):

            self.compute_legalmoves(idx==1)
            action = self.Agents[self.turn].playcard(self.get_gameknowledge())


            if self.islegal(action):
                self.Hand[self.turn].playcard(action)
            else:
                action = random.choice(self.legalmoves)
                self.Hand[self.turn].playcard(action)

            if action in pointcards:
                self.breakheart = True

            if position == 0:
                self.currentType = action.color

            card_played.append( (self.turn,action) )

            self.turn += 1
            self.turn %= 4
            
        print(card_played)

        return card_played

    def start(self):
        for idx in range(1,14):
            card_played = self.rounds(idx)
            score = sum([pointcards[c[1]] for c in card_played if c[1] in pointcards])

            card_played = [c for c in card_played if c[1].color == self.currentType]

            #reset round
            max_card = min(card_played, key = lambda x: card_order.index(x[1].number) )
            start = max_card[0]
            self.score[start] += score
            self.turn = start
            self.currentType = None

        # pig goat
        for idx in range(4):
            if self.score[idx] == 26:
                self.score[idx] = -26
                break

        return self.score

    def get_gameknowledge(self):
        #
        self.gameknowledge["legalmoves"] =  self.legalmoves[:]
        self.gameknowledge["cards_left"] = self.Hand[self.turn].Cards[:]
        self.gameknowledge["turn"] = self.turn
        return self.gameknowledge
    
    def changecard(self,cardslist):
        for idx,cards in enumerate(cardslist):
            if len(cards) != 3 or any(c not in self.Hand[idx].Cards for c in cards):
                cardslist[idx] = random.sample(self.Hand[idx].Cards, 3)
                
            if idx != 0:
                #remove change cards
                for c in cardslist[idx]:
                    self.Hand[idx].Cards.remove(c)
                
                for c in cardslist[idx-1]:
                    self.Hand[idx].Cards.append(c)
                
        for c in cardslist[0]:
            self.Hand[0].Cards.remove(c)
                
        for c in cardslist[3]:
            self.Hand[0].Cards.append(c)
            
        for i in range(4):
            self.Hand[i].order()
    
    
    def compute_legalmoves(self,first):
        self.legalmoves = []
        hand = self.Hand[self.turn].Cards

        # No point Card Can Be played at the first roind
        if first:
            if self.currentType:
                self.legalmoves = [c for c in hand if c.color == self.currentType and c not in pointcards]
            else:
                self.legalmoves = [Card(Colored.CLUB,2)]
        elif self.breakheart:
            if self.currentType:
                self.legalmoves = [c for c in hand if c.color == self.currentType]
            else:
                self.legalmoves = [c for c in hand]
        else:
            if self.currentType:
                self.legalmoves = [c for c in hand if c.color == self.currentType and c not in pointcards]
            else:
                self.legalmoves = [c for c in hand if c not in pointcards]

        # if there is nothing to do, play any card you want
        self.legalmoves = self.legalmoves if self.legalmoves else [c for c in hand]

    def islegal(self,action):
        return True if action in self.legalmoves else False

'''
gameknowlede is dictionary
legalmoves
gamehistory 
left cards
'''

class easy_agent(object):
    def __init__(self):
        pass
    
    def playcard(self,gameknowledge):
        return random.choice(gameknowledge["legalmoves"])
    
    def changecard(self,cards):
        return random.sample(cards,3)


if __name__=="__main__":
    Onegame = Game()
    result = Onegame.start()
    print("\n".join(["player %d : %d" %(idx,r) for idx,r in enumerate(result) ]))
