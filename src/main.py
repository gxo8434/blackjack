class Game:
    def __init__(self):
        deck = Deck()
        dealer = Dealer()
        gambler = Gambler()

class Deck:
    def __init__(self):
        self.init_cards()
        self.shuffle_cards()

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

def main():
    pass

if __name__ == '__main__':
    main()
