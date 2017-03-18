import sys
import itertools
import numpy as np
import copy

class Pedro_Card(object):
    """ Playing card for Pedro
    
    Attributes:
        suit: string 
            hearts / diamonds / spades / clubs
        rank: integer 
            value between 2-14 e.g. 14 = Ace
        color: string
            black or red
        suit_rank: int 
            used for sorting hands for easy visualization
        sort_rank: int
            used for sorting hands. pedros (5s)
            get special rank since they can belong 
            to either suit which matches their color
    """

    SUIT_RANKS = {'hearts':1,'diamonds':2,'spades':3,'clubs':4}
    FACES = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
    COLORS = {'hearts': 'red', 'diamonds': 'red',
              'spades': 'black', 'clubs': 'black'}

    def __init__(self, rank, suit):
        """ initialize Pedro Card

        args:
            rank: integer
            suit: string
        """

        self.suit = suit
        self.rank = rank
        self.color = self.COLORS[suit.lower()]
        self.suit_rank = self.SUIT_RANKS[suit]
        self.sort_rank = rank
        if rank == 5:
            if self.suit_rank == 1 or self.suit_rank == 3:
                self.sort_rank = 100
            else:
                self.sort_rank = 0

    def points(self, trump_suit):
        """ Point value of card

        args:
            trump_suit: string
        returns: int
            point value of card
        """

        singles = set([2, 10, 11, 14])
        if self.trump(trump_suit):
            if self.rank in singles:
                return 1
            elif self.rank == 5:
                return 5
            else:
                return 0
        else:
            return 0
    
    def trump(self, trump_suit):
        """ check if card is trump

        args:
            trump_suit: string
        return bool:
            True if trump
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

    def __eq__(self, card):
        if self.rank == card.rank and self.suit == card.suit:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __str__(self):
        value = self.FACES.get(self.rank, self.rank)
        return "{0} of {1}".format(value, self.suit)

    def __repr__(self):
        return str(self)

class Pedro_Hand:
    """ Pedro Hand

    attributes:
        cards: list 
            list of Pedro_Cards in hand
        name: string
            player name associated with hand
        trump: list
            list of trump cards in hand
        offsuit: list
            list of offsuit cards in hand
        suits: set
            set of all suits in hand
    """
    # Expectation Values
    EVs = {}
    EVs['deuce'] = 1
    EVs['ace'] = 4.
    EVs['ace_king'] = 5.6
    EVs['ace_king_queen'] = 8.01
    EVs['ace_king_queen_jack'] = 12.
    EVs['jack_fourth'] = 1.
    EVs['ten_fifth'] = 1.
    EVs['jack_third'] = 0.5
    EVs['ten_fourth'] = 0.5
    EVs['pedro_fifth'] = 2.5
    EVs['pedro_sixth'] = 4.

    def __init__(self, name='Player', cards=[]):
        """ initialize Pedro Hand

        args:
            name: string 
                player name
            cards: iterable of Pedro_Cards
                initial cards in hand
                defaults to empyt list
        """

        self.cards = copy.deepcopy(cards)
        self.name = name
        self.trump = []
        self.offsuits = []
        self.bid_suit = ''
        self.suits = set()

    def size(self):
        """ Returns number of cards in hand"""

        return len(self.cards)

    def play(self, loc_of_card):
        """ Plays a card

        args:
            loc_of_card: int
                position of card to be played
        """
        return self.cards.pop(loc_of_card)

    def sort(self):
        """ sorts hand by grouping by suit"""

        self.cards = sorted(self.cards,key=lambda 
                            x:(x.suit_rank,x.sort_rank))

    def sort_by_points(self, trump_suit):
        """ sorts hand by point value of cards

        args:
            trump_suit: string
        """

        self.cards = sorted(self.cards,key=lambda 
                            x:(x.points(trump_suit), 
                               x.rank),
                               reverse=True)

    def clear(self):
        """ deletes all cards from hand"""

        self.cards = []

    def discard(self, trump_suit):
        """ discards all offsuit cards

        args:
           trump_suit: string
        return:
            list of discarded cards
        """
        
        cards = []
        discarded = []
        for card in self.cards:
            if card.trump(trump_suit):
                cards.append(card)
            else:
                discarded.append(card)
        self.cards = cards
        return discarded

    def split(self, trump_suit):
        """ splits hand by trump / offsuit
        
        splits hand into 
        trump cards and offsuit cards
        and builds set of all suits in hand
        sets trump / suits / offsuit
        attributes of hand

        args:
                trump_suit: string

        """
        self.trump = []
        self.trump_cards = set()
        self.offsuit = []
        self.suits = set()
        for pos, card in enumerate(self.cards):
            if card.trump(trump_suit):
                self.trump.append((pos,card))
                self.suits.add(trump_suit)
                self.trump_cards.add(card)
            else:
                self.offsuit.append((pos, card))
                self.suits.add(card.suit)

    def where(self, suit):
        """ which offcards match suit

        args:
            suit: string
        returns list:
            list of tuples (position of card, card) 
            of cards which match suit
        """

        matches = []
        for pos, card in self.offsuit:
            if card.suit == suit:
                matches.append((pos,card))
        return matches

    def filter(self, trump_suit):
        ace = Pedro_Card(14, trump_suit)
        king = Pedro_Card(13, trump_suit)
        queen = Pedro_Card(12, trump_suit)
        jack = Pedro_Card(11, trump_suit)
        ten = Pedro_Card(10, trump_suit)
        deuce = Pedro_Card(2, trump_suit)
        pedro1 = Pedro_Card(5, trump_suit)
        if trump_suit == 'hearts':
            tmp = 'diamonds'
        elif trump_suit == 'diamonds':
            tmp = 'hearts'
        elif trump_suit == 'clubs':
            tmp = 'spades'
        elif trump_suit == 'spades':
            tmp = 'clubs'
        pedro2 = Pedro_Card(5, tmp)
        num_pedros = 0
        ace_in = False
        king_in = False
        queen_in = False
        jack_in = False
        deuce_in = False
        ten_in = False

        num_trumps = len(self.trump)
        if ace in self.trump_cards:
            ace_in = True
        if king in self.trump_cards:
            king_in = True
        if queen in self.trump_cards:
            queen_in = True
        if deuce in self.trump_cards:
            deuce_in = True
        if jack in self.trump_cards:
            jack_in = True
        if ten in self.trump_cards:
            ten_in = True
        if pedro1 in self.trump_cards:
            num_pedros += 1
        if pedro2 in self.trump_cards:
            num_pedros += 1
        
        value = 0
        if ace_in and king_in and queen_in and jack_in:
            value += self.EVs['ace_king_queen_jack']
        elif ace_in and king_in and queen_in:
            value += self.EVs['ace_king_queen']
        elif ace_in and king_in:
            value += self.EVs['ace_king']
        elif ace_in:
            value += self.EVs['ace'] + (num_trumps-2)

        if deuce_in:
            value += self.EVs['deuce']

        if num_pedros == 1:
            if num_trumps == 6:
                value += self.EVs['pedro_sixth']
            elif num_trumps == 5:
                value += self.EVs['pedro_fifth']
        if num_trumps >=3:
            if jack_in and num_trumps == 4:
                value += self.EVs['jack_fourth']
            elif jack_in and num_trumps == 3:
                value += self.EVs['jack_third']
            if ten_in and num_trumps == 5:
                value += self.EVs['ten_fifth']
            elif ten_in and num_trumps == 4:
                value += self.EVs['ten_fourth']
        return value

    def bid(self):
        suits = ['hearts',
                 'clubs',
                 'diamonds',
                 'spades']
        values = np.zeros(4)
        for i, suit in enumerate(suits):
            self.split(suit)
            values[i] = self.filter(suit)
        self.bid_suit = suits[np.argmax(values)]
        bid = int(round(np.amax(values)))
        if bid > 14:
            bid = 14
        if bid < 6:
            bid = 0
        return bid


    def __add__(self, cards_to_add):
        if not isinstance(cards_to_add, Pedro_Hand):
            cards_to_add = Pedro_Hand(cards=cards_to_add)
        self.cards += cards_to_add.cards
        return self

    def __str__(self):
        s = self.name+'\n'
        for i, card in enumerate(self.cards):
            s = s + '  ' + str(i) + ': ' + str(card) + '\n'
        return s[:-1]

    def __repr__(self):
        return str(self)

class Deck:
    """ Deck of Pedro_Cards 
        initializes unshuffled deck of cards 
    """

    def __init__(self):
        ranks = range(2, 15)
        suits = 'spades diamonds clubs hearts'.split()
        self.cards = [Pedro_Card(r, s) for s, r in
                      itertools.product(suits, ranks)]

    def shuffle(self):
        """ shuffle cards"""
        np.random.shuffle(self.cards)

    def deal(self, number_of_cards):
        """ Removes number_of_cards from deck 
            And returns Hand_of_Cards
            if number_of_cards > len(deck.cards):
                returns number_of_cards
            else:
                returns remaining cards
        """
        dealt_cards = []
        for i in range(number_of_cards):
            try:
                dealt_cards.append(self.cards.pop())
            except IndexError:
                pass
        return dealt_cards

class Pedro_Game:
    
    def __init__(self):

        self.deck = Deck()
        #self.deck.shuffle()

        self.teams=(0,1,0,1)
        self.players = [Pedro_Hand(name='A'),
                        Pedro_Hand(name='B'),
                        Pedro_Hand(name='C'),
                        Pedro_Hand(name='D')]

        # Order of dealer rotation
        self.orders = itertools.cycle([
                            (0, 1, 2, 3),
                            (1, 2, 3, 0),
                            (2, 3, 0, 1),
                            (3, 0, 1, 2)])
        
    def start(self):
        """Runs the game"""

        score = [0, 0]
        for order in self.orders:
            self.deal_hand(order)
            bid, winning_bidder = self.bidding(order)
            pos = order[winning_bidder]
            # Dont let computer pass deck
            if bid == 0:
                bid = 6
                #print 'Passed Deck\n'
                #team = self.teams[pos]
                #score[team] -= 6
            #else:
            # replace with cpu selection of trump
            #print self.players[pos]
            trump_suit = self.players[pos].bid_suit
            #trump_suit = raw_input('Trump?\n')
            #print 'Winning Bid / Trump Suit'
            #print bid, '/', trump_suit

            # discard all offsuit cards
            self.discard_offsuit(order, trump_suit)
            
            # play tricks
            team1, team2 = self.play_round(pos, trump_suit)
            if pos == 0 or pos == 2:
                # team1 won bid
                print bid, team1
                if bid == 14 and team1 == 14:
                    score[0] += 28
                else:
                    score[1] += team2
                    if team1 >= bid:
                        score[0] += team1
                    else:
                        score[0] -= bid
            else:
                # team2 won bid
                print bid, team2
                if bid == 14 and team2 == 14:
                    score[1] += 28
                else:
                    score[0] += team1
                    if team2 >= bid:
                        score[1] += team2
                    else:
                        score[1] -= bid
            print score
            if score[0] >= 1000000 or score[1] >= 1000000:
                print 'Game Over'
                print score
                break

            print 'Score:'
            print '  {} {}\n'.format(*score)
            self.reset()

    def play_round(self, pos, trump_suit):
        lead_suit = trump_suit
        points_played = 0
        team1 = 0
        team2 = 0
        for count in range(6):
            # Playing Order is winning bidder for first trick
            # then winner or last trick
            trick = [0 for i in range(4)]
            order = [i for i in range(pos,4)] + [
                     i for i in range(0,pos)]
            for i, pos in enumerate(order):
                self.players[pos].split(trump_suit)
                if count == 0:
                    # Must be trump card for first trick
                    allowed_locs = self.players[pos].trump

                    # Need to handle rare case of more than 6 trumps
                    # discard non-point cards to get down to 5
                    num_trumps = len(allowed_locs)
                    if num_trumps > 6:
                        # sort hand by points then rank
                        self.players[pos].sort_by_points(trump_suit)
                        excess = num_trumps - 6
                        # discard lowest non-point trumps 
                        # to get back to 6 cards
                        print 'More than 6 trumps'
                        print 'Discarded:'
                        for i in range(excess):
                            discard = self.players[pos].play(num_trumps - 1 - i)
                            print '',discard
                        self.players[pos].split(trump_suit)
                        allowed_locs = self.players[pos].trump
                else:
                    if i == 0:
                        # first player can play any card
                        allowed_locs = self.players[pos].trump + self.players[pos].offsuit
                    else:
                        if lead_suit == trump_suit:
                            allowed_locs = self.players[pos].trump
                        else:
                            if lead_suit in self.players[pos].suits:
                                # must follow suit if possible 
                                # but can always trump
                                allowed_locs = (self.players[pos].where(lead_suit) 
                                                + self.players[pos].trump)
                            else:
                                # any card if can't follow suit
                                allowed_locs = self.players[pos].trump + self.players[pos].offsuit
                if allowed_locs:
                    #print self.players[pos]
                    #print allowed_locs
                    #loc = int(raw_input('Card?\n'))
                    # Get random play
                    np.random.shuffle(allowed_locs)
                    loc = allowed_locs[0][0]
                    card = self.players[pos].play(loc)
                    if i == 0:
                        lead_suit = card.suit
                    points_played += card.points(trump_suit)
                    trick[i] = card
                    if card.points(trump_suit) and card.rank == 2:
                        # the Deuce
                        if pos == 0 or pos == 2:
                            team1 += 1
                        else:
                            team2 += 1
                else:
                    self.players[pos].clear()
            # pos -> person that wins trick
            #self.print_trick(order, trick)
            winner, trick_points = self.check_trick(trick, trump_suit, lead_suit)
            pos = order[winner]
            # Quick scoring implementation
            if pos == 0 or pos == 2:
                team1 += trick_points
            else:
                team2 += trick_points
            #print self.players[pos].name, 'won the trick'
            #print trick_points
            if points_played == 14:
                return team1, team2
        return team1, team2

    def print_trick(self, order, trick):
        line1 = '{:20}{:>20}'.format(
                self.players[order[0]].name,
                self.players[order[1]].name)
        line4 = '{:20}{:>20}'.format(
                self.players[order[2]].name,
                self.players[order[3]].name)
        line2 = '{:>20}  {:20}'.format(trick[0],trick[1])
        line3 = '{:>20}  {:20}'.format(trick[3],trick[2])
        print
        print line1
        print line2
        print line3
        print line4
        print

    def check_trick(self, trick, trump_suit, lead_suit, show=False):
        card_vals = np.zeros(4, dtype=int)
        trick_points = 0
        for i, card in enumerate(trick):
            try:
                card_val = card.rank
                if card.trump(trump_suit):
                    card_val *= 100
                if card.suit == trump_suit:
                    card_val *= 10
                if card.suit == lead_suit:
                    card_val *= 10
                card_vals[i] = card_val
                if card.rank != 2 or card.suit != trump_suit:
                    # Not the deuce / deuce makes itself
                    trick_points += card.points(trump_suit)
            except AttributeError:
                # Player with no valid cards
                pass
        winner = np.argmax(card_vals)
        return winner, trick_points

    def discard_offsuit(self, order, trump_suit):
        """All players discard offsuit cards 
           and are dealt back to 6 cards total
        """
            
        #cards_left = 52 - 4*9
        for i, pos in enumerate(order):
            if i < 3:
                # All players but the dealer discard their offsuit
                # cards. Then get dealt back to 6 cards
                discarded = self.players[pos].discard(trump_suit)
                cards_needed = 6 - self.players[pos].size()
                if cards_needed > 0:
                    dealt = self.deck.deal(cards_needed)
                    num_dealt = len(dealt)
                    self.players[pos] += dealt
                    diff = cards_needed - num_dealt
                    if diff > 0:
                        self.players[pos] += discarded[:diff]

                    
                    
                    #if cards_left >= cards_needed:
                    #    self.players[pos] += dealt
                    #    cards_left -= cards_needed
                    #else:
                    #    # If Deck runs out
                    #    # fill hand with discards
                    #    num_dealt = len(dealt)
                    #    self.players[pos] += dealt
                    #    diff = cards_needed - num_dealt
                    #    self.players[pos] += discarded[:diff]
                    #    cards_left -= num_dealt
            else:
                # Dealer gets remainder of deck 
                # then discards down to 6 cards
                cards_left = len(self.deck.cards)
                dealt = self.deck.deal(cards_left)
                self.players[pos] += dealt 
                discarded = self.players[pos].discard(trump_suit)
                cards_needed = 6 - self.players[pos].size()
                if cards_needed > 0:
                    self.players[pos] += discarded[:cards_needed]

    def deal_hand(self, order):
        for i in range(3):
            for j in range(4):
                dealt_cards = self.deck.deal(3)
                pos = order[j]
                self.players[pos] += dealt_cards

    def reset(self):
        # Clear All Hands
        for i in range(4):
            self.players[i].clear()
        # New Shuffled Deck
        self.deck = Deck()
        self.deck.shuffle()

    def bidding(self, order):
        min_bid = 6
        max_bid = 14
        for i, pos in enumerate(order):
            self.players[pos].sort()
            # Prints hand and gets input 
            # from command line for bidding
            # will be replaced by cpu
            #print self.players[pos]
            if i == 3 and min_bid == 6:
                bids = [0, 6, 14]
                #bid = int(raw_input(str(bids) + '\n'))
                bid = self.players[pos].bid()
                return bid, i
            bid = 0
            if min_bid > 14:
                if i == 3:
                    bids = [0, 14]
                    #bid = int(raw_input(str(bids) + '\n'))
                    bid = self.players[pos].bid()
                    if bid == 14:
                        return 14, 3
            else:
                bids = [0] + range(min_bid, max_bid + 1)
                #bid = int(raw_input(str(bids) + '\n'))
                bid = self.players[pos].bid()
            if bid >= min_bid:
                current_bid = bid
                min_bid = current_bid + 1
                loc = i 
        return current_bid, loc

