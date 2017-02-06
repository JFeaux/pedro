from itertools import product
from random import shuffle
from PIL import ImageTk, Image


class Card:
    FACES = {11: 'jack', 12: 'queen', 13: 'king', 14: 'ace'}
    COLORS = {
        'hearts': 'red',
        'diamonds': 'red',
        'spades': 'black',
        'clubs': 'black'}

    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.color = self.COLORS[suit.lower()]

    def __str__(self):
        value = self.FACES.get(self.rank, self.rank)
        return "{0} of {1}".format(value, self.suit)

    def __repr__(self):
        return str(self)

    def check_trump(self, trump_suit, game):
        if game == 'pedro':
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
        else:
            print 'Error: '
            print '  Only rules for pedro have been implemented'
            sys.exit(1)

    def set_image(self, path_to_deck, scale=0.5):
        """
        Gets .png file for card.
        Scales and opens self.image
        Requires tkinter root initialized
        """

        image_file = path_to_deck
        value = self.FACES.get(self.rank, self.rank)
        image_file += '{}_of_{}.png'.format(value, self.suit.lower())
        self.image_file = image_file

        self.SCALE = scale
        self.HEIGHT = self.SCALE * 251.0
        self.WIDTH = self.SCALE * 180.0

        image = Image.open(self.image_file)
        self.image = ImageTk.PhotoImage(
            image.resize(
                (int(
                    self.WIDTH), int(
                    self.HEIGHT)), Image.ANTIALIAS))


class Deck:
    """ Deck of Cards """

    def __init__(self):
        ranks = range(2, 15)
        suits = 'spades diamonds clubs hearts'.split()
        self.cards = [Card(r, s) for s, r in product(suits, ranks)]

    def __str__(self):
        s = ''
        for i in range(len(self.cards)):
            s = s + ' ' * i + str(self.cards[i]) + '\n'
        return s

    def __repr__(self):
        pass

    def shuffle(self):
        shuffle(self.cards)

    def deal(self, hand, num_cards=1):
        for i in range(num_cards):
            hand.add(self.cards.pop())
