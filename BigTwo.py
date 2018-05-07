from enum import Enum
import random
from collections import defaultdict


class Colored(Enum):
    SPADE = "spade"
    HEART = "heart"
    DIAMOND = "diamond"
    CLUB = "club"
    
class Card(object):
    
    
    def __init__(self,color,number):
        self.color = color
        self.number = number
        
    def __str__(self):
        return str(self.color)+" "+str(self.number)
    def __repr__(self):
        return self.color.value+" "+str(self.number)
    
    def __eq__(self,Other):
        
        if not isinstance(Other,Card):
            return False
        
        if self.color == Other.color and self.number == Other.number:
            return True
        return False
    
#each player has 13 cards
card_order =  [2,1,13,12,11,10,9,8,7,6,5,4,3]
card_color = [Colored.SPADE,Colored.HEART,Colored.DIAMOND,Colored.CLUB]
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
    indexX = card_order.index(x.number)
    indexY = card_order.index(y.number)
    
    if indexX < indexY:
        return 1
    elif indexX > indexY:
        return -1
    else:
        indexX = card_color.index(x.color)
        indexY = card_color.index(y.color)
        
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
        self.legalmoves = self.computelegal()
    def order(self):
        self.Cards = sorted(self.Cards,key=cmp_to_key(card_cmp))
    def computelegal(self,MyHand=None):
        
        MyHand = self.Cards if MyHand == None else MyHand
        card_collect = defaultdict(lambda: [])
        card_number = dict([(i,0) for i in range(1,14)])
        for c in MyHand:
            card_collect[c.number].append(c)
            card_number[c.number] +=1
        card_sequence = [i for i in range(1,14) if card_number[i] > 0]
        ones = [[c] for c in MyHand]
        pairs = []
        for key in card_collect:
            length = card_number[key]
            if length>=2:
                pairs.extend( [(card_collect[key][A],card_collect[key][B]) 
                    for A in range(length-1)
                    for B in range(A+1,length)
                    ])
        fullhouse = []
        for key in card_collect:
            length = card_number[key]
            if length>=3:
                fullhouse.extend([
                    (pair[0],pair[1],card_collect[key][A],card_collect[key][B],card_collect[key][C]) 
                    for pair in [p for p in pairs if p[0].number != key]
                    for A in range(length-2)
                    for B in range(A+1,length-1)
                    for C in range(B+1,length)
                ])
        flush = []
        i = card_sequence[0] if len(card_sequence) > 0 else 11
        while i<=10:
            link = True
            a = 1
            while link:
                if i+a == 14 and 1 in card_sequence:
                    flush.extend([
                       (cardA,cardB,cardC,cardD,cardE)
                        for cardA in card_collect[10]
                        for cardB in card_collect[11]
                        for cardC in card_collect[12]
                        for cardD in card_collect[13]
                        for cardE in card_collect[1]
                    ])
                    i+=1
                elif (i+a) not in card_sequence:
                    i = i+a+1
                    link = False
                    continue
                elif a==4:
                    if i!=2:
                        flush.extend([
                           (cardA,cardB,cardC,cardD,cardE)
                            for cardA in card_collect[i]
                            for cardB in card_collect[i+1]
                            for cardC in card_collect[i+2]
                            for cardD in card_collect[i+3]
                            for cardE in card_collect[i+4]
                        ])
                    else:
                        flush.extend([
                           (cardB,cardC,cardD,cardE,cardA)
                            for cardA in card_collect[i]
                            for cardB in card_collect[i+1]
                            for cardC in card_collect[i+2]
                            for cardD in card_collect[i+3]
                            for cardE in card_collect[i+4]
                        ])
                    i+=1
                else:
                    a+=1
        fourking = []
        for key in card_collect:
            length = card_number[key]
            if length>=4:
                fourking.extend([
                    (One[0],card_collect[key][0],card_collect[key][1],card_collect[key][2],card_collect[key][3]) 
                    for One in [o for o in ones if o[0].number != key]
                ])
        straightflush = []
        for f in flush:
            if (f[0].color == f[1].color and f[0].color == f[1].color 
            and f[0].color == f[2].color and f[0].color == f[3].color):
                straightflush.append(f)
        
        for f in straightflush:
            flush.remove(f)
        
        return {'ones':ones,'pairs':pairs,'fullhouse':fullhouse,
                'flush':flush,'fourking':fourking,'straightflush':straightflush}
        
        
    def islegal(self,move):
        if move == "pass":
            return True
        
        for moves in self.legalmoves:
            if move in moves:
                return True
        return False
    
    def playcard(self,action):
        if action=="pass": return
        
        for c in action:
            self.Cards.remove(c)
            
        self.legalmoves = self.computelegal()
            

def easy_agent(game_knowledge):
        
        legal_moves = game_knowledge['legal_moves']
        
        
        for t in ['fullhouse','flush','pairs']:
            if len(legal_moves[t]) > 0:
                return (t,legal_moves[t][0])

        for t in legal_moves:
            if len(legal_moves[t]) > 0:
                return (t,legal_moves[t][0])
        
        return ("pass","pass")


class Game(object):
    
    def __init__(self):
        self.set_game()
    def set_game(self):
        Poker = [Card(color,num) for num in  card_order for color in card_color]
        random.shuffle(Poker)
        
        print("Start Order Cards")
        self.Hand = [player(Poker[:13]),player(Poker[13:26]),player(Poker[26:39]),player(Poker[39:])]
        self.turn = 0
        for i in range(3):
            if Card(Colored.CLUB,3) in self.Hand[i].Cards:
                break
            self.turn+=1
        self.all_pass = True
        self.currentType = None
        self.currentCard = None
        self.passes = 3
        self.gamehistory = []
        self.Agents = [easy_agent for i in range(4)]
        self.round = 1
        
        print("Game Start")
        
            
    def rounds(self):
        action = self.Agents[self.turn](self.get_gameknowledge() )
        return action if self.islegal(action) else ("pass","pass")
    
    def start(self):
        while True:
            action_type, action = self.rounds()
            self.Hand[self.turn].playcard(action)
            self.gamehistory.append( (action_type, action))

            print(self.round,action_type,action)
            if action != "pass":
                self.all_pass = False
                self.passes = 0
                self.currentType = action_type
                self.currentCard = action
            elif self.passes == 2:
                self.all_pass = True
                self.currentType = None
                self.currentCard = None
            else:
                self.passes += 1 
            if len(self.Hand[self.turn].Cards) == 0:
                return [len(self.Hand[i].Cards) for i in range(4)]


            self.round += 1
            self.turn += 1
            self.turn %= 4

            if self.round >=100:
                return [len(self.Hand[i].Cards) for i in range(4)]
        
    def get_gameknowledge(self):
        #
        self.gameknowledge = dict()
        if self.all_pass:
            self.gameknowledge['legal_moves']  = self.Hand[self.turn].legalmoves
        else:
            legal_moves = defaultdict(lambda: [])
            legal_moves[self.currentType] = [ move
                                            for move in self.Hand[self.turn].legalmoves[self.currentType]
                                            if card_cmp(self.currentCard[-1],move[-1]) == -1
            ]
            if self.currentType in ['ones','pairs','fullhouse','flush']:
                legal_moves['fourking'] = self.Hand[self.turn].legalmoves['fourking']
                legal_moves['straightflush'] = self.Hand[self.turn].legalmoves['straightflush']
            
            elif self.currentType == 'fourking':
                legal_moves['straightflush'] = self.Hand[self.turn].legalmoves['straightflush']
                
            
            self.gameknowledge['legal_moves'] = legal_moves
        
        return self.gameknowledge
    
    def islegal(self,action):
        if ("pass","pass"): return True
        
        for moves in self.gameknowledge['legal_moves']:
            if action in moves:
                return True
        return False
    '''
    def set_game_from_card_list(Poker)
        self.Agents = [player(Poker[:13]),player(Poker[13:26]),player(Poker[26:39]),player(Poker[:39])]
    '''


if __name__ == "__main__":
    Onegame = Game()
    result = Onegame.start()
    print(result)
