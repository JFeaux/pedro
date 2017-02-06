#!/usr/bin/python

import sys
import os
import random

# tkinter modules
import Tkinter as tk
import tkFont
import tkSimpleDialog
import tkMessageBox

# Custom Modules
from card_tools import Deck


class Pedro_Player:

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.dealer = False

    def clear_hand(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def discard(self, trump_suit):
        self.cards = [
            card for card in self.cards if card.check_trump(
                trump_suit, 'pedro')]

    def card_rank(self, card):
        sort_rank = card.rank
        if card.rank == 5:
            if card.suit == 'clubs' or card.suit == 'diamonds':
                sort_rank = 100
            else:
                sort_rank = 0
        return card.color[0], card.suit[0], sort_rank

    def sort_hand(self):
        self.cards = sorted(self.cards, key=self.card_rank)

    def set_dealer(self):
        self.dealer = True

    def __str__(self):
        s = self.name + '\n'
        for i in range(len(self.cards)):
            s = s + ' ' + str(i + 1) + ':' + ' ' * (i + 1) + \
                str(self.cards[i]) + '\n'
        return s

    def get_label(self, frame, fontsize=12, fontcolor='white'):
        font_style = tkFont.Font(family='Times', size=fontsize)
        label = tk.Label(
            frame,
            text=self.name,
            bg='forest green',
            fg=fontcolor,
            font=font_style)
        return label

    def hand_as_image(self, frame):

        if len(self.cards) == 0:
            return None

        width = self.cards[0].WIDTH
        height = self.cards[0].HEIGHT

        dx = width / 4.
        x_center = width / 2.
        y_center = height / 2.

        num_cards = len(self.cards)
        hand_frame = tk.Canvas(frame, width=dx * (num_cards - 1) + width,
                               height=height, bg='forest green')
        for count, card in enumerate(self.cards):
            shift = count * dx
            hand_frame.create_image(
                shift + x_center, y_center, image=card.image)
        return hand_frame

    def bidding(self, pedro_game, order_loc, current_bid, winning_bid_loc):
        for count, button in enumerate(self.buttons):
            if count == 0:
                if not self.dealer:
                    button['state'] = tk.NORMAL
                else:
                    if current_bid == 5:
                        button['state'] = tk.NORMAL
            else:
                bid = count + 5
                if bid > current_bid:
                    button['state'] = tk.NORMAL

    def bid_frame(self, frame):
        self.buttons = []
        button_font = tkFont.Font(family='Times', size=16)
        bid_frame = tk.Frame(frame)
        bids = [i for i in range(6, 15)]

        if self.dealer:
            text = 'Pass Deck'
            b = tk.Button(bid_frame, text=text, font=button_font, command=quit)
            self.buttons.append(b)
            b['state'] = tk.DISABLED
            b.pack(side='left')
            for bid in bids:
                b = tk.Button(
                    bid_frame,
                    text=bid,
                    font=button_font,
                    command=quit)
                self.buttons.append(b)
                b.pack(side='left')
                b['state'] = tk.DISABLED
        else:
            text = 'Pass'
            b = tk.Button(
                bid_frame,
                text=text,
                font=button_font,
                command=lambda: game.get_bid(
                    game.order_loc,
                    game.current_bid,
                    game.winning_bid_loc))
            self.buttons.append(b)
            b.pack(side='left')
            b['state'] = tk.DISABLED
            for bid in bids:
                b = tk.Button(
                    bid_frame,
                    text=bid,
                    font=button_font,
                    command=lambda bid=bid: game.get_bid(
                        game.order_loc + 1,
                        bid,
                        game.order_loc))
                self.buttons.append(b)
                b.pack(side='left')
                b['state'] = tk.DISABLED

        return bid_frame


class Pedro_Game:

    def __init__(self, root, team1, team2):

        p1a = Pedro_Player(team1[0])
        p1b = Pedro_Player(team1[1])
        p2a = Pedro_Player(team2[0])
        p2b = Pedro_Player(team2[1])
        self.players = [p1a, p2a, p1b, p2b]

    def build_deck(self, path):
        self.deck = Deck()
        for card in self.deck.cards:
            card.set_image(path, scale=0.5)
        self.deck.shuffle()

    def pick_dealer(self):
        temp = random.randint(0, 3)
        order = [0, 1, 2, 3]
        self.order = order[temp:] + order[0:temp]
        self.dealer_pos = self.order[3]
        self.players[self.dealer_pos].set_dealer()

        string = self.players[self.dealer_pos].name + ' will deal first'
        tkMessageBox.showinfo(root, string)

        self.deal_round()

    def deal_round(self):
        for i in range(3):
            for loc in self.order:
                player = self.players[loc]
                self.deck.deal(player, 3)
        # build board
        player_locs = [
            (0, 0),
            (0, 1),
            (4, 1),
            (4, 0)]
        for count, player in enumerate(self.players):
            player.sort_hand()
            x, y = player_locs[count]
            player.get_label(frame).grid(row=x, column=y)
            player.hand_as_image(frame).grid(row=x + 1, column=y, rowspan=2)
            player.bid_frame(frame).grid(row=x + 3, column=y)
        vert_spacer = tk.Label(frame, text='\n\n\n\n', bg='forest green')
        vert_spacer.grid(row=3, column=0)

        self.get_bid(0, 5, 0)

    def get_bid(self, order_loc, current_bid, winning_bidder_loc):
        self.order_loc = order_loc
        self.current_bid = current_bid
        self.winning_bidder_loc = winning_bidder_loc
        loc = self.order[order_loc]
        player = self.players[loc]
        player.bidding(self, order_loc, current_bid, winning_bidder_loc)


random.seed(1)

# Initialize tkinter
root = tk.Tk()
root.title('Pedro')

# Get screen properties from root
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
frame = tk.Frame(
    root,
    height=screen_height,
    width=screen_width,
    bg='forest green',
    borderwidth=10,
    relief='ridge')

# Initialize Game with Player Names
# Change to GUI input
team1 = ('Jacob', 'Mom')
team2 = ('David', 'Brigette')
game = Pedro_Game(root, team1, team2)

# Needs to be generalized with variable
path = '/home/jacob/git/pedro/deck/'
game.build_deck(path)

game.pick_dealer()


# jacob,david,mom,brigette=players
#
# deck.deal(jacob,9)
# deck.deal(david,9)
# deck.deal(mom,9)
# deck.deal(brigette,9)
#
#
# fontsize=20
# fontcolor='white'
#
# spacers=[
#    tk.Label(frame,text='          ',bg='forest green'),
#    tk.Label(frame,text='          ',bg='forest green'),
#    tk.Label(frame,text='          ',bg='forest green')]
#
# height=jacob.cards[0].HEIGHT
# width=jacob.cards[0].WIDTH
#
# player_locs=[
#    (0,0),
#    (0,5),
#    (8,5),
#    (8,0)]
#
# spacer_locs=[
#    (0,1),
#    (0,4),
#    (0,6)]
#
#
# jacob.set_dealer()
#
#
# for count,spacer in enumerate(spacers):
#  x,y=spacer_locs[count]
#  spacer.grid(row=x,column=y)
#

# trick1=tk.Canvas(frame,width=width,height=height)
# trick2=tk.Canvas(frame,width=width,height=height)
# trick3=tk.Canvas(frame,width=width,height=height)
# trick4=tk.Canvas(frame,width=width,height=height)
#
# trick_locs=[
#    (4,2),
#    (4,3),
#    (6,2),
#    (6,3)]
# trick1.grid(row=4,column=2,rowspan=2)
# trick2.grid(row=4,column=3,rowspan=2)
# trick3.grid(row=6,column=2,rowspan=2)
# trick4.grid(row=6,column=3,rowspan=2)


frame.pack()
root.mainloop()

#  def show_hand(self,frame):
#    label=tk.Label(frame,text=self.name)
#    label.pack(side='top')
#
#    width=self.hand.cards[0].WIDTH
#    dx=width/4.
#    height=self.hand.cards[0].HEIGHT
#    x_center=width/2.
#    y_center=height/2.
#
#    num_cards=len(self.hand.cards)
#    card_frame=tk.Canvas(frame,width=dx*(num_cards+2),
#      height=height)
#    for count,card in enumerate(self.hand.cards):
#      shift=count*dx
#      card_frame.create_image(shift+x_center,y_center,image=card.image)
#    card_frame.pack(side='top')
