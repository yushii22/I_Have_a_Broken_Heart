class player(object):

    # list of 13 cards
    def __init__(self, cards):
        self.cards = cards
        self.order()

    def order(self):
        self.cards = sorted(self.cards, key=cmp_to_key(card_cmp))

    def playcard(self, card):
        self.cards.remove(card)
        return 0
