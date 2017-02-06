#!/usr/bin/python

import os
import sys
import random
import time

from itertools import product

import Tkinter as tk
import tkFont
import tkSimpleDialog
import tkMessageBox

from PIL import ImageTk, Image


class Card:
    FACES = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
    SUITS = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}
    COLORS = {'Hearts': 0, 'Diamonds': 0, 'Spades': 1, 'Clubs': 1}

    def __init__(self, rank, suit, scale=0.6):
        self.suit = suit
        self.rank = rank

        self.suit_rank = self.SUITS[suit]
        self.sort_rank = self.rank
        if rank == 5:
            if self.suit_rank == 1 or self.suit_rank == 3:
                self.sort_rank = 100
            else:
                self.sort_rank = 0

        image_file = '/home/jacob/personal/card_game/deck/'
        image_file += '{:>02}'.format(self.rank) + suit[0].lower() + '.png'
        self.image_file = image_file

        # self.HEIGHT=self.SCALE*251.0
        # self.WIDTH=self.SCALE*180.0

        self.SCALE = scale
        self.HEIGHT = 251.0
        self.WIDTH = 180.0

        self.image = Image.open(self.image_file)
        self.photo_image = ImageTk.PhotoImage(self.image.resize(
            (int(self.SCALE * self.WIDTH), int(self.SCALE * self.HEIGHT)), Image.ANTIALIAS))

    def __str__(self):
        value = self.FACES.get(self.rank, self.rank)
        return "{0} of {1}".format(value, self.suit)

    def __repr__(self):
        return str(self)

    def resize(self, scale):
        self.scale = scale
        self.photo_image = ImageTk.PhotoImage(self.image.resize(
            (int(scale * self.WIDTH), int(scale * self.HEIGHT)), Image.ANTIALIAS))

    def show(self):
        os.system('eog ' + self.image_file)

    def check_trump(self, trump_suit):
        if self.rank != 5:
            if self.suit == trump_suit:
                return True
            else:
                return False
        else:
            if self.COLORS[self.suit] == self.COLORS[trump_suit]:
                return True
            else:
                return False


class Hand:

    def __init__(self):
        self.cards = []

    def clear_hand(self):
        self.cards = []

    def discard(self, trump_suit):
        self.cards = [x for x in self.cards if x.check_trump(trump_suit)]

    def sort_hand(self):
        self.cards = sorted(
            self.cards, key=lambda x: (
                x.suit_rank, x.sort_rank))

    def play(self, card):
        return self.cards.pop(card - 1)

    def add(self, card):
        self.cards.append(card)

    def __str__(self):
        s = ''
        for i in range(len(self.cards)):
            s = s + ' ' + str(i + 1) + ':' + ' ' * (i + 1) + \
                str(self.cards[i]) + '\n'
        return s

    def __repr__(self):
        return str(self)


class Deck:

    def __init__(self, scale=0.6):
        ranks = range(2, 15)
        suits = 'Spades Diamonds Clubs Hearts'.split()
        self.cards = [Card(r, s, scale=scale)
                      for s, r in product(suits, ranks)]
        self.scale = scale

    def __str__(self):
        s = ''
        for i in range(len(self.cards)):
            s = s + ' ' * i + str(self.cards[i]) + '\n'
        return s

    def __repr__(self):
        pass

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, hand, num_cards=1):
        for i in range(num_cards):
            hand.add(self.cards.pop())


class Pedro_Player:

    def __init__(self, name, position):
        self.name = name
        self.hand = Hand()
        self.dealer = False
        self.position = position

    def get_label(self, frame, fontsize, fontcolor):

        font_style = tkFont.Font(family='Times', size=fontsize)
        label = tk.Label(
            frame,
            text=self.name,
            bg='forest green',
            fg=fontcolor,
            font=font_style)
        return label

    def set_dealer(self):
        self.dealer = True

    def hand_as_image(self, frame, scale=0.5):

        if len(self.hand.cards) == 0:
            return None

        for card in self.hand.cards:
            card.resize(scale)

        width = self.hand.cards[0].WIDTH * scale
        height = self.hand.cards[0].HEIGHT * scale

        dx = width / 4.
        x_center = width / 2.
        y_center = height / 2.

        num_cards = len(self.hand.cards)
        hand_frame = tk.Canvas(frame, width=dx * (num_cards - 1) + width,
                               height=height, bg='forest green')
        for count, card in enumerate(self.hand.cards):
            shift = count * dx
            hand_frame.create_image(
                shift + x_center,
                y_center,
                image=card.photo_image)

        return hand_frame

    def hand_as_button(self, frame, scale=0.5):

        if len(self.hand.cards) == 0:
            return None

        for card in self.hand.cards:
            card.resize(scale)

        width = self.hand.cards[0].WIDTH * scale
        height = self.hand.cards[0].HEIGHT * scale

        dx = width / 4.
        x_center = width / 2.
        y_center = height / 2.

        hand_frame = tk.Frame(frame,
                              height=height, bg='forest green')

        num_cards = len(self.hand.cards)
        buttons = [0 for i in range(num_cards)]
        for count, card in enumerate(self.hand.cards):
            shift = count * dx
            if count == len(self.hand.cards) - 1:
                buttons[count] = tk.Button(
                    hand_frame,
                    height=height,
                    width=width,
                    image=card.photo_image,
                    command=quit)
            else:
                buttons[count] = tk.Button(
                    hand_frame,
                    height=height,
                    width=dx,
                    image=card.photo_image,
                    command=quit)
            buttons[count].grid(row=0, column=count)

        return hand_frame


class Pedro_Game:

    def __init__(self, root, deck, players):
        self.root = root
        self.deck = deck
        self.dealer_pos = 3
        self.order = [0, 1, 2, 3]
        self.players = players

        # Get Size Parameter from Cards
        # scale=deck.cards[0].scale
        self.height, self.width = deck.cards[0].HEIGHT, deck.cards[0].WIDTH

    def pick_dealer(self):
        temp = random.randint(0, 3)
        self.order = self.order[temp:] + self.order[0:temp]
        self.dealer_pos = self.order[3]
        self.players[self.dealer_pos].set_dealer()

        string = self.players[self.dealer_pos].name + ' will deal first'
        tkMessageBox.showinfo(root, string)
        self.deal()

    def get_bid(self, order_loc, current_bid, winning_bidder_loc):
        loc = self.order[order_loc]
        try:
            self.hand_frame.destroy()
        except AttributeError:
            pass
        player = self.players[loc]
        player.hand.sort_hand()

        dx = self.width / 4.
        x_center = self.width / 2.
        y_center = self.height / 2.

        self.hand_frame = tk.Frame(root)
        player.hand_as_image(self.hand_frame)

        button_font = tkFont.Font(family='Times', size=16)
        bid_frame = tk.Frame(self.hand_frame)
        text = 'Pass'
        if player.dealer:
            if current_bid == 5:
                text = 'Pass Deck'
                bids = [6, 14]
            elif current_bid == 14:
                bids = [14]
            else:
                bids = [current_bid + 1, 14]
        else:
            if current_bid < 14:
                bids = [i for i in range(6, 15)]
            else:
                self.get_bid(3, 14, winning_bidder_loc)

        if player.dealer:
            b = tk.Button(
                bid_frame,
                text=text,
                font=button_font,
                command=lambda: self.select_trump(
                    current_bid,
                    winning_bidder_loc))
            b.pack(side='left')
            for bid in bids:
                b = tk.Button(
                    bid_frame,
                    text=bid,
                    font=button_font,
                    command=lambda bid=bid: self.select_trump(
                        bid,
                        order_loc))
                b.pack(side='left')
        else:
            b = tk.Button(
                bid_frame,
                text=text,
                font=button_font,
                command=lambda: self.get_bid(
                    order_loc + 1,
                    current_bid,
                    winning_bidder_loc))
            b.pack(side='left')
            for bid in bids:
                b = tk.Button(
                    bid_frame,
                    text=bid,
                    font=button_font,
                    command=lambda bid=bid: self.get_bid(
                        order_loc + 1,
                        bid,
                        order_loc))
                b.pack(side='left')
                if bid < current_bid + 1:
                    b['state'] = tk.DISABLED
        bid_frame.pack(side='bottom')
        self.hand_frame.pack()

    def select_trump(self, winning_bid, winning_bidder_loc):
        winning_bidder_loc = self.order[winning_bidder_loc]

        winning_bidder = self.players[winning_bidder_loc]
        name = winning_bidder.name
        self.hand_frame.destroy()

        dx = self.width / 4.
        x_center = self.width / 2.
        y_center = self.height / 2.

        self.hand_frame = tk.Frame(self.root)

        winning_bidder.hand_as_image(self.hand_frame)

        suits = 'Hearts Diamonds Spades Clubs'.split()
        lower_frame = tk.Frame(self.hand_frame)
        for suit in suits:
            b = tk.Button(
                lower_frame,
                text=suit,
                command=lambda suit=suit: self.play_hand(
                    winning_bid,
                    winning_bidder_loc,
                    suit))
            b.pack(side='left')
        lower_frame.pack()
        self.hand_frame.pack()

    def play_hand(self, winning_bid, winning_bidder_loc, trump_suit):
        self.hand_frame.destroy()
        order = [0, 1, 2, 3]
        self.order = order[winning_bidder_loc:] + order[:winning_bidder_loc]

        for loc in self.order:
            player = self.players[loc]
            player.hand.discard(trump_suit)
            num_cards = len(player.hand.cards)
            need = 6 - num_cards
            if need > 0:
                self.deck.deal(player.hand, need)
            player.hand.sort_hand()

        # for count,loc in enumerate(self.order):
        player = self.players[winning_bidder_loc]
        player.hand_as_button(root, winning_bidder_loc)

    def deal(self):
        for i in range(3):
            for loc in self.order:
                player = self.players[loc]
                self.deck.deal(player.hand, 3)
        self.get_bid(0, 5, 0)


class Trick:

    def __init__(self, trump_suit):
        self.trump_suit = trump_suit
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def old_trick(self, frame, scale=0.25):
        if len(self.cards) == 0:
            return None

        for card in self.cards:
            card.resize(scale)

        width = self.cards[0].WIDTH * scale
        height = self.cards[0].HEIGHT * scale

        x_center = width / 2.
        y_center = height / 2.

        num_cards = len(self.cards)
        hand_frame = tk.Canvas(frame, width=num_cards * width,
                               height=height, bg='forest green')
        for count, card in enumerate(self.cards):
            hand_frame.create_image(
                width * count + x_center,
                y_center,
                image=card.photo_image)

        return hand_frame


scale = 0.5
random.seed(1)

root = tk.Tk()
root.title('Pedro')

screen_height = root.winfo_screenwidth()
screen_width = root.winfo_screenheight()

frame = tk.Frame(
    root,
    height=screen_height,
    width=screen_width,
    bg='forest green',
    borderwidth=10,
    relief='ridge')

deck = Deck(scale=scale)
deck.shuffle()

players = [
    Pedro_Player('Jacob', 0),
    Pedro_Player('David', 1),
    Pedro_Player('Mom', 2),
    Pedro_Player('Brigette', 3)]

jacob, david, mom, brigette = players

deck.deal(jacob.hand, 4)
deck.deal(david.hand, 4)
deck.deal(mom.hand, 4)
deck.deal(brigette.hand, 4)

fontsize = 20
fontcolor = 'white'

spacers = [
    tk.Label(frame, text='          ', bg='forest green'),
    tk.Label(frame, text='          ', bg='forest green'),
    tk.Label(frame, text='          ', bg='forest green')]

height = jacob.hand.cards[0].HEIGHT
width = jacob.hand.cards[0].WIDTH

player_locs = [
    (0, 0),
    (0, 5),
    (7, 5),
    (7, 0)]

trick_locs = [
    (3, 2),
    (3, 3),
    (5, 2),
    (5, 3)]

spacer_locs = [
    (0, 1),
    (0, 4),
    (0, 6)]

current_trick = Trick('Hearts')
deck.deal(current_trick, 4)

trick1 = tk.Canvas(frame, width=scale * height, height=scale * height)
trick2 = tk.Canvas(frame, width=scale * height, height=scale * height)
trick3 = tk.Canvas(frame, width=scale * height, height=scale * height)
trick4 = tk.Canvas(frame, width=scale * height, height=scale * height)

x_center = width * scale
y_center = height * scale


test = [
    tk.Label(frame, image=current_trick.cards[0].photo_image),
    tk.Label(frame, image=current_trick.cards[1].photo_image),
    tk.Label(frame, image=current_trick.cards[2].photo_image),
    tk.Label(frame, image=current_trick.cards[3].photo_image)]


names = [
    jacob.get_label(frame, fontsize, fontcolor),
    david.get_label(frame, fontsize, fontcolor),
    mom.get_label(frame, fontsize, fontcolor),
    brigette.get_label(frame, fontsize, fontcolor)]

hands = [
    jacob.hand_as_button(frame, scale=0.5),
    david.hand_as_image(frame, scale=0.5),
    mom.hand_as_image(frame, scale=0.5),
    brigette.hand_as_image(frame, scale=0.5)]

for count, name in enumerate(names):
    x, y = player_locs[count]
    name.grid(row=x, column=y)
    hands[count].grid(row=x + 1, column=y, rowspan=2)

for count, t in enumerate(test):
    x, y = trick_locs[count]
    t.grid(row=x, column=y, rowspan=2)

for count, spacer in enumerate(spacers):
    x, y = spacer_locs[count]
    spacer.grid(row=x, column=y)

played_trick = Trick('Hearts')
deck.deal(played_trick, 4)
played = played_trick.old_trick(frame)
played.grid(row=1, column=7)

# layed_trick=Trick('Clubs')
# deck.deal(layed_trick,4)
# layed=layed_trick.old_trick(frame)
# layed.grid(row=2,column=7)


# old trick = column 7


frame.pack()

# game=Pedro_Game(root,deck,players)

# game.pick_dealer()

root.mainloop()
