import sys
import itertools
import numpy as np


class Card(object):
    """ Playing Card """

    SUITS={'hearts':1,'diamonds':2,'spades':3,'clubs':4}
    FACES = {11: 'jack', 12: 'queen', 13: 'king', 14: 'ace'}
    COLORS = {'hearts': 'red', 'diamonds': 'red',
              'spades': 'black', 'clubs': 'black'}

    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.color = self.COLORS[suit.lower()]

        self.suit_rank = self.SUITS[suit]
        self.sort_rank = self.rank

    def __str__(self):
        value = self.FACES.get(self.rank, self.rank)
        return "{0} of {1}".format(value, self.suit)

    def __repr__(self):
        return str(self)

class Pedro_Card(Card):
    """ Playing card for pedro"""

    def __init__(self, rank, suit):
        Card.__init__(self, rank, suit)

        if rank == 5:
            if self.suit_rank == 1 or self.suit_rank == 3:
                self.sort_rank = 100
            else:
                self.sort_rank = 0

    def points(self, trump_suit):
        if self.check_trump(trump_suit):
            if rank == 2 or rank == 10 or rank == 11 or rank == 14:
                return 1
            elif rank == 5:
                return 5
            else:
                return 0
        else:
            return 0

    
    def check_trump(self, trump_suit):
        """ check if card matches trump suit
        """
        if self.rank != 5:
            # If card is not pedro / does suit match
            if self.suit == trump_suit:
                return True
            else:
                return False
        else:
            # If card is pedro / does color match
            trump_color = self.COLORS[trump_suit.lower()]
            if self.color == trump_color:
                return True
            else:
                return False

class Hand_of_Cards(object):
    """ Hand of Cards 
        initialize with an iterable of cards /
        defaults to empty hand
    """

    def __init__(self, cards=[]):
        self.cards = cards

    def size(self):
        return len(self.cards)

    def play(self, loc_of_card):
        return self.cards.pop(loc_of_card)

    def sort(self):
        self.cards=sorted(self.cards,key=lambda 
                          x:(x.suit_rank,x.sort_rank))

    def where(self, suit, trump = False):
        pos = []
        for i, card in enumerate(self.cards):
            for suit in suits:
                if card.check_trump(suit):
                    pos.append(i)
                    break
        return pos

    def discard(self, trump_suit):
        cards = []
        for card in self.cards:
            if card.check_trump(trump_suit):
                cards.append(card)
        self.cards = cards

    def clear(self):
        self.cards = []


    def __add__(self, new_cards):
        return Hand_of_Cards(self.cards + new_cards.cards)

    def __str__(self):
        if self.size() == 0:
            return 'Empty'
        else:
            s = ''
            for i, card in enumerate(self.cards):
                s = s + str(i) + ': ' + str(card) + '\n'
            return s[:-1]

    def __repr__(self):
        return str(self)


class Deck(Hand_of_Cards):
    """ Deck of Cards 
        initializes unshuffled deck of cards 
    """

    def __init__(self, game='Pedro'):
        ranks = range(2, 15)
        suits = 'spades diamonds clubs hearts'.split()
        if game == 'Pedro':
            self.cards = [Pedro_Card(r, s) for s, r in
                      itertools.product(suits, ranks)]

    def shuffle(self):
        """ shuffle cards"""
        np.random.shuffle(self.cards)

    def deal(self, number_of_cards):
        """ Removes number_of_cards from deck 
            And returns Hand_of_Cards
        """
        dealt_cards = []
        for i in range(number_of_cards):
            dealt_cards.append(self.cards.pop())
        return Hand_of_Cards(dealt_cards)

class Pedro_Game:
    
    def __init__(self):

        self.deck = Deck(game='Pedro')
        self.deck.shuffle()

        self.players = [Hand_of_Cards(),
                        Hand_of_Cards(),
                        Hand_of_Cards(),
                        Hand_of_Cards()]

        self.dealer_pos = itertools.cycle((3,0,1,2))

        self.orders = [(1,2,3,0),
                       (2,3,0,1),
                       (3,0,1,2),
                       (0,1,2,3)]
                        
    def deal_hand(self, dealer_pos):
        order = self.orders[dealer_pos]
        for i in range(3):
            for j in range(4):
                pos = order[j]
                dealt_cards = self.deck.deal(3)
                self.players[pos] += dealt_cards

    def bidding(self, dealer_pos):
        order = self.orders[dealer_pos]
        current_bid = 5
        for i in range(4):
            if current_bid == 14:
                if i == 3:
                    tmp = np.random.random()
                    if tmp > 0.8:
                        winning_loc = i
            else:
                bid = int(round(np.random.normal(7,3),0))
                if bid >= 14:
                    current_bid = 14
                    winning_loc = i
                elif bid > current_bid:
                    if current_bid < 7:
                        current_bid = 7
                    else:
                        current_bid += 1
                    winning_loc = i
        if current_bid == 5:
            return 6, 3
        else:
            return current_bid, winning_loc

    def reset(self):
        self.deck = Deck(game='Pedro')
        self.deck.shuffle()
        for i in range(4):
            self.players[i].clear()

    def redeal(self,dealer_loc):
        orders = self.orders[dealer_loc]
        for i in range(4):
            pos = orders[i]
            self.players[pos].discard(trump_suit)
            cards_needed = 6 - self.players[pos].size()
            if cards_needed > 0:
                dealt_cards = game.deck.deal(cards_needed)
                self.players[pos] += dealt_cards
    
    def play_tricks(self, count, order, trump_suit):
        """ function to go through process of playing tricks
            may split into different rounds
            and I need function to determine winner of trick which 
            returns location of winner
        """
        order = list(order)
        trick = [0 for i in range(4)]
        if count == 0:
            for i, pos in enumerate(order):
                trump_locs = self.players[pos].where_trump(trump_suit, trump_suit)
                if trump_locs:
                    np.random.shuffle(trump_locs)

                    card = self.players[pos].play(trump_locs[0])
                    trick[i] = card

                    size = self.players[pos].size()
                    if size > 5:
                        diff = size - 5
                        for i in range(diff):
                            loop = True
                            repeat = 0
                            while loop:
                                card = self.players[pos].cards[trump_locs[i+1+repeat]]
                                if card.points == 0:
                                    loop = False
                                    self.players[pos].play(trump_locs[i+1+repeat])
                                repeat += 1
                else:
                    order.pop(pos)
            print trick
        else:
            # order determined by last winner
            trick = [0 for i in range(4)] 
            order = [i for i in range(loc,4)] + [i for i in range(loc)]
            for i, pos in enumerate(order):
                # Just play first card / Needs revision for strategy
                if i == 0:
                    card = self.players[pos].play(0)
                    lead_suit = card.suit
                    trick[i] = card
                else:
                    # This function is incorrect 
                    # Need to implement function similar to np.where 
                    # if lead_suit is off card / must first 
                    # follow suit / if can't follow suit any suit allowed
                    # if lead_suit is trump must play trump
                    allowed_locs = self.players[pos].where_trump(lead_suit, trump_suit)
                    if allowed_locs:
                        np.random.shuffle(allowed_locs)
                        card = self.players[pos].play(allowed_locs[0])
                        trick[i] = card
                    else:
                        order.pop(pos)
            print trick

class Pedro_Trick:
    """ Functions which enforce 
        pedro rules for a trick
    """

    def __init__(self, trump_suit, lead_suit):
        self.trump_suit = trump_suit
        self.lead_suit = lead_suit

    def where(self, hand, first_trick = False, lead_player = False):
        if first_play:
            pass
        else:
            pass






                
                



def rank_hand(hand):
    hand_rank = hand.size()
    for card in hand.cards:
        if card.rank == 14:
            hand_rank += 2
        if card.rank == 2:
            hand_rank += 1
        if card.rank == 13:
            hand_rank += 1
        if card.rank == 12:
            hand_rank += 1
        return hand_rank

def choose_trump(hand):
    ranks = [0 for i in range(4)]
    suits = hand.cards[0].SUITS.keys()
    for i, suit in enumerate(suits):
        tmp_hand = Hand_of_Cards()
        tmp_hand += hand
        tmp_hand.discard(suit)
        ranks[i] = rank_hand(tmp_hand)
    return suits[np.argmax(ranks)]


np.random.seed(1)



game = Pedro_Game()


rounds = 0
for pos in game.dealer_pos:
    game.deal_hand(pos)

    bid, loc = game.bidding(pos)
    trump_suit = choose_trump(game.players[loc])

    game.redeal(pos)

    order = [i for i in range(loc,4)] + [i for i in range(loc)]
    # play_tricks not yet implemented
    for i in range(6):
        game.play_tricks(i, order, trump_suit)

    rounds += 1
    if rounds > 0:
        break
    game.reset()


