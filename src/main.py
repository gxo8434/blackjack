class Game:
    def __init__(self):
        deck = Deck()
        dealer = Dealer()
        player = Player()



class Deck:
    def __init__(self):
        self.init_cards()
        self.shuffle_cards()

class Dealer:
    def __init__(self):
        hand = Hand()

class Player:
    def __init__(self):
        hand = Hand()

class Hand:
    def __init__(self):
        pass

def main():
    pass

if __name__ == '__main__':
    main()
