# -*- coding: utf-8 -*-
from agent import Agent
import random
from game import Game



class MyAgent(Agent):
    def play(self, cards_you_have, cards_played, heart_broken, info):
        legal_moves = Game.get_legal_moves(cards_you_have, cards_played, heart_broken)
        return self.get_good_moves(cards_you_have, cards_played, heart_broken, legal_moves)

    def pass_cards(self, cards):
        spade = 0
        diamond = 0
        club = 0
        spade_list = []
        diamond_list = []
        club_list = []
        cards_list = []
        for card in cards:
            cards_list.append(card)
        for card in cards:
            if card.suit == '♠':
                spade += 1
                spade_list.append(card)
            elif card.suit == '♦':
                diamond += 1
                diamond_list.append(card)
            elif card.suit == '♣':
                club += 1
                club_list.append(card)
            else:
                heart = 0
        cards_should_pass = []
        if len(spade_list) <= 2:
            cards_should_pass = cards_should_pass + spade_list
            
        if len(diamond_list) <= 2:
            cards_should_pass = cards_should_pass + diamond_list
            
        if len(club_list) <= 2:
            cards_should_pass = cards_should_pass + club_list
            
        if len(cards_should_pass) >= 3:
            return random.sample(cards_should_pass, 3)
        elif int(len(cards_should_pass)) == 2:
            a = cards_should_pass[0]
            cards_list.remove(a)
            b = cards_should_pass[1]
            cards_list.remove(b)
            c = random.choice(cards_list)
            cards_should_pass.append(c)
            return cards_should_pass
        elif int(len(cards_should_pass)) == 1:
            a = cards_should_pass[0] 
            cards_list.remove(a)
            b = random.choice(cards_list)
            cards_list.remove(b)
            cards_should_pass.append(b)
            c = random.choice(cards_list)
            cards_should_pass.append(c)
            return cards_should_pass
        else:
            return random.sample(cards, 3)

    def score(self, cards):
        total_score = 0
        for card in cards:
            if card.suit == '♥':
                total_score += 1
            elif card == '♠12':
                total_score += 13
        return total_score

    def get_good_moves(self, cards_you_have, cards_played, heart_broken, legal_moves):
        if not cards_played:
            all_numbers = [int(card.number) for card in legal_moves]
            min_number = min(all_numbers)
            result = []
            for card in legal_moves:
                if card.number == min_number:
                    result.append(card)
            return random.choice(result)
        else:
            suit = cards_played[0].suit
            all_numbers = [int(card.number) for card in cards_played if card.suit == suit]
            max_number = 1 if 1 in all_numbers else max(all_numbers)
            card_score = {}
            for card in legal_moves:
                card_num = int(card.number)
                card_suit = card.suit
                total_score = self.score(cards_played + [card])
                if ((card_suit == suit and card_num == 1) 
                    or (card_suit == suit and card_num > max_number and max_number != 1)
                   ):
                    card_score[card] = total_score
                else:
                    card_score[card] = 0
            good_moves = []
            good_moves = [card for card in legal_moves if card_score[card] == min(card_score.values())]
            all__numbers = [int(card.number) for card in good_moves]
            max__number = 1 if 1 in all__numbers else max(all__numbers)
            result = []
            for card in good_moves:
                card_num = int(card.number)
                if card_num == max__number:
                    result.append(card)
            return random.choice(result)


        
