class Game:
    def __init__(self):
        deck = Deck()
        dealer = Dealer()
        gambler = Gambler()

    def deal(player):
        card = deck.draw()
        player.hand.add(card)

class Deck:
    def __init__(self):
        self.init_cards()
        self.shuffle()

    def init_cards(self):
        pass

    def shuffle(self):
        pass

    def draw():
        # Draw card
        pass

class Card:
    def __init__(self):
        pass

class Player:
    def __init__(self):
        hand = Hand()

class Dealer(Player):
    def __init__(self):
        super.__init__(self)

class Gambler(Player):
    def __init__(self):
        super.__init__(self)

class Hand:
    def __init__(self):
        pass
    
    def add(self, card):
        # Add card to hand
        pass

def main():
    pass

if __name__ == '__main__':
    main()
