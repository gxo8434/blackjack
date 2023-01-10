# An implementation of Blackjack, to run in your terminal
# Sean Reid

import random

# Game implements the flow of the game
class Game:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer()
        self.gambler = Gambler(100)
        self.reset()
    
    # turn implements a series of hits for both gambler and dealer
    def turn(self):
        while not self.gambler.finished:
            print(str(self))
            self.gambler.action(self.deck)
    
        while not self.dealer.game_over():
            print(str(self))
            self.dealer.deal(self.deck)

    # reset redeals and sets wager to 0
    def reset(self):
        self.deck = Deck()
        self.dealer.hand = Hand()
        self.gambler.hand = Hand()
        self.gambler.wager = 0
        self.gambler.finished = False
        self.dealer.deal(self.deck, hide=True)
        self.dealer.deal(self.deck)
        for _ in range(2):
            self.gambler.deal(self.deck)
    
    # plays the game until you run out of money
    def play(self):
        while self.gambler.funds > 0:
            print(str(self))
            self.gambler.gamble()
            self.turn()
            self.show_cards()
            print(str(self))
            win = self.gambler_win()
            self.print_outcome(win)
            self.reset()
       print('You are out of money. Time to stop!')

    # reveals the dealer's hidden card
    def show_cards(self):
        for card in self.dealer.hand.cards:
            self.dealer.hand.cards[card] = 'shown'
    
    # prints the outcome of the game
    def print_outcome(self, win):
        if win:
            self.gambler.funds += self.gambler.wager
            print('You Win!')
        else:
            self.gambler.funds -= self.gambler.wager
            print('You Lose!')
        print('')
    
    # calculates who wins
    def gambler_win(self):
        if self.gambler.over():
            return False
        elif self.dealer.over():
            return True
        else:
            dscore = self.dealer.hand.max_score()
            gscore = self.gambler.hand.max_score()
            if dscore < gscore:
                return True
            else:
                return False
    
    # displays the game state
    def __str__(self):
        return f'Wager: {self.gambler.wager}\nDEALER\'S HAND\n{self.dealer.hand}\nGAMBLER\'S HAND\n{self.gambler.hand}\n'

# Deck implements a 52 card deck
class Deck:

    suits = ['H', 'S', 'C', 'D']
    maxnum = 13

    def __init__(self):
        self.init_cards()
        self.shuffle()

    # iterate through all suits and numbers (Ace has value 1) and assign them to the deck
    def init_cards(self):
        self.cards = []
        for suit in self.suits:
            for number in range(1, self.maxnum + 1):
                card = Card(number, suit)
                self.cards.append(card)
    
    # randomize deck
    def shuffle(self):
        random.shuffle(self.cards)

    # draw a card
    def draw(self):
        # Draw card
        card = self.cards.pop()
        return card

# Defines the properties of a card
class Card:

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    # Displays the card nicely on the terminal
    def __str__(self):
        if self.number == 1:
            val = ' A'
        elif self.number == 11:
            val = ' J'
        elif self.number == 12:
            val = ' Q'
        elif self.number == 13:
            val = ' K'
        else:
            val = f'{self.number:>2}'
        if self.suit == 'H':
            suit = '♥'
        elif self.suit == 'S':
            suit = '♠'
        elif self.suit == 'C':
            suit = '♣'
        elif self.suit == 'D':
            suit = '♦'
        return f'-------\n|     |\n|     |\n|     |\n| {val}{suit} |\n|     |\n|     |\n|     |\n-------'

# Base class, extended to gambler and dealer
class Player:
    def __init__(self):
        self.hand = Hand()

    # Deal card from deck to player. If hidden, card is not displayed in terminal
    def deal(self, deck, hide=False):
        card = deck.draw()
        self.hand.add(card, hide)

    # Game is over if score is over 21
    def over(self):
        scores = self.hand.scores()
        for score in scores:
            if score <= 21:
                return False
        return True

# Dealer comes equipped with a special game over function
class Dealer(Player):
    def __init__(self):
        super().__init__()

    # game is over when the dealer reaches a score of over 17
    def game_over(self):
        scores = self.hand.scores()
        for score in scores:
            if score >= 17:
                return True
        return False

# Gambler is the user interface to wagering and making actions in the game
class Gambler(Player):
    def __init__(self, funds):
        super().__init__()
        self.funds = funds # start with some amount of money
        self.wager = 0 # how much to bet
        self.finished = False # set to true when done with turn

    # Choose either hit, stand or double down. TODO: implement split action
    def action(self, deck):
        action = input('\nSpecify an action from the list below.\n1. Hit (take a card)\n2. Stand (take no cards and end turn)\n3. Double Down (double wager, take one more card, and end turn)\n\nChoose a number from 1 to 3: ')
        action_int = int(action)
        if action_int not in [1, 2, 3]:
            print('\nEnter a number from 1 to 3')
            self.action(deck)
        if action_int == 2:
            self.finished = True
            print('')
            return
        elif action_int == 3:
            self.wager *= 2
            self.deal(deck)
            self.finished = True
        elif action_int == 1:
            self.deal(deck)
            if self.over():
                self.finished = True
        print('')
    
    # wager some amount
    def gamble(self):
        amount = input(f'How much to wager? You have {self.funds} left.\nEnter numerical value here ($): ')
        amount_int = int(amount)
        if amount_int == 0:
            print('\nEnter non-zero dollar amount.')
            self.gamble()
        self.wager += int(amount)
        print('')

# Hand is a collection of cards equipped with scoring
class Hand:
    def __init__(self):
        self.cards = {}
    
    # put a new card in the hand, maybe hidden
    def add(self, card, hide=False):
        if hide:
            self.cards[card] = 'hidden'
        else:
            self.cards[card] = 'shown'

    # calculate all possible scores, including branches for different values of Ace.
    def scores(self):
        scores = [0]
        for card in self.cards:
            if card.number == 1:
                scores_tmp = []
                for score in scores:
                    scores_tmp.append(score + 11)
                    scores_tmp.append(score + 1)
                scores = scores_tmp
            else:
                if card.number > 10:
                    value = 10
                else:
                    value = card.number
                for ii, score in enumerate(scores):
                    scores[ii] += value
        return scores

    # Max score without going above 21.
    def max_score(self):
        s = 0
        for score in self.scores():
            if score > 21:
                continue
            elif score > s:
                s = score
        return s
    
    # Format hand prettily
    def __str__(self):
        handstr = []
        for card in self.cards:
            if self.cards[card] == 'hidden':
                handstr.append('-------\n|     |\n|     |\n|     |\n|     |\n|     |\n|     |\n|     |\n-------'.split('\n'))
            else:
                handstr.append(str(card).split('\n'))
        return '\n'.join([' '.join(elem) for elem in zip(*handstr)])

# Play game
def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
