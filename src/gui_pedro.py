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
  FACES = {11: 'jack', 12: 'queen', 13: 'king', 14: 'ace'}
  SUITS = {'hearts':1,'diamonds':2,'spades':3,'clubs':4}
  COLORS = {'hearts':0,'diamonds':0,'spades':1,'clubs':1}

  def __init__(self, rank, suit,scale=0.75):
    self.suit = suit
    self.rank = rank

    self.suit_rank=self.SUITS[suit]
    self.sort_rank=self.rank
    if rank == 5:
      if self.suit_rank == 1 or self.suit_rank == 3:
        self.sort_rank=100
      else:
        self.sort_rank=0

    image_file='/home/jacob/personal/card_game/deck/'
    image_file+='{:>02}'.format(self.rank)+suit[0].lower()+'.png'
    self.image_file=image_file

    self.SCALE=scale
    self.HEIGHT=self.SCALE*251.0
    self.WIDTH=self.SCALE*180.0

    image = Image.open(self.image_file)
    self.image=ImageTk.PhotoImage(image.resize((int(self.WIDTH),int(self.HEIGHT)),Image.ANTIALIAS))

  def __str__(self):
    value = self.FACES.get(self.rank, self.rank)
    return "{0} of {1}".format(value, self.suit)

  def __repr__(self):
    return str(self)

  def show(self):
    os.system('eog '+self.image_file)

  def check_trump(self,trump_suit):
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
    self.cards=[]

  def clear_hand(self):
    self.cards=[]

  def discard(self,trump_suit):
    self.cards=[x for x in self.cards if x.check_trump(trump_suit)]

  def sort_hand(self):
    self.cards=sorted(self.cards,key=lambda x:(x.suit_rank,x.sort_rank))

  def play(self,card):
    return self.cards.pop(card-1)

  def add(self,card):
    self.cards.append(card)

  def __str__(self):
    s=''
    for i in range(len(self.cards)):
      s=s + ' '+str(i+1)+':'+' ' * (i+1) + str(self.cards[i]) + '\n'
    return s

  def __repr__(self):
    return str(self)

class Deck:

  def __init__(self,scale=0.75):
    ranks=range(2,15)
    suits='Spades Diamonds Clubs Hearts'.split()
    self.cards=[Card(r,s,scale=scale) for s,r in product(suits,ranks)]
    self.scale=scale

  def __str__(self):
    s=''
    for i in range(len(self.cards)):
      s=s + ' ' * i + str(self.cards[i]) + '\n'
    return s

  def __repr__(self):
    pass

  def shuffle(self):
    random.shuffle(self.cards)

  def deal(self,hand,num_cards=1):
    for i in range(num_cards):
      hand.add(self.cards.pop())

class Pedro_Player:
  def __init__(self,name):
    self.name=name
    self.hand=Hand()
    self.dealer=False

  def set_dealer(self):
    self.dealer=True

  def show_hand(self,frame):
    label=tk.Label(frame,text=self.name)
    label.pack(side='top')

    width=self.hand.cards[0].WIDTH
    dx=width/4.
    height=self.hand.cards[0].HEIGHT
    x_center=width/2.
    y_center=height/2.

    num_cards=len(self.hand.cards)
    card_frame=tk.Canvas(frame,width=dx*(num_cards+2),
      height=height)
    for count,card in enumerate(self.hand.cards):
      shift=count*dx
      card_frame.create_image(shift+x_center,y_center,image=card.image)
    card_frame.pack(side='top')


  def play_card(self,root,loc):

    width=self.hand.cards[0].WIDTH
    dx=width/4.
    height=self.hand.cards[0].HEIGHT
    x_center=width/2.
    y_center=height/2.

    hand_frame=tk.Frame(root,
        height=height)
    label=tk.Label(hand_frame,text=self.name)

    num_cards=len(self.hand.cards)
    buttons=[0 for i in range(num_cards)]
    for count,card in enumerate(self.hand.cards):
      shift=count*dx
      if count == len(self.hand.cards) - 1:
        buttons[count]=tk.Button(hand_frame,height=height,
            width=width,image=card.image,command=quit)
      else:
        buttons[count]=tk.Button(hand_frame,height=height,
            width=dx,image=card.image,command=quit)
      buttons[count].pack(side='left')
    hand_frame.pack(anchor=tk.CENTER)

class Pedro_Game:
  def __init__(self,root,deck,players):
    self.root=root
    self.deck=deck
    self.dealer_pos=3
    self.order=[0,1,2,3]
    self.players=players
    

    # Get Size Parameter from Cards
    #scale=deck.cards[0].scale
    self.height,self.width=deck.cards[0].HEIGHT,deck.cards[0].WIDTH

  def pick_dealer(self):
    temp=random.randint(0,3)
    self.order=self.order[temp:]+self.order[0:temp]
    self.dealer_pos=self.order[3]
    self.players[self.dealer_pos].set_dealer()

    string=self.players[self.dealer_pos].name+' will deal first'
    tkMessageBox.showinfo(root,string)
    self.deal()

  def get_bid(self,order_loc,current_bid,winning_bidder_loc):
    loc=self.order[order_loc]
    try:
      self.hand_frame.destroy()
    except AttributeError:
      pass
    player=self.players[loc]
    player.hand.sort_hand()

    dx=self.width/4.
    x_center=self.width/2.
    y_center=self.height/2.

    self.hand_frame=tk.Frame(root)
    player.show_hand(self.hand_frame)

    button_font=tkFont.Font(family='Times',size=16)
    bid_frame=tk.Frame(self.hand_frame)
    text='Pass'
    if player.dealer:
      if current_bid == 5:
        text='Pass Deck'
        bids=[6,14]
      elif current_bid == 14:
        bids=[14]
      else:
        bids=[current_bid+1,14]
    else:
      if current_bid < 14:
        bids=[i for i in range(6,15)]
      else:
        self.get_bid(3,14,winning_bidder_loc)

    if player.dealer:
      b=tk.Button(bid_frame,text=text,font=button_font,command=lambda: self.select_trump(current_bid,winning_bidder_loc))
      b.pack(side='left')
      for bid in bids:
        b=tk.Button(bid_frame,text=bid,font=button_font,command=lambda bid=bid: self.select_trump(bid,order_loc))
        b.pack(side='left')
    else:
      b=tk.Button(bid_frame,text=text,font=button_font,command=lambda: self.get_bid(order_loc+1,current_bid,winning_bidder_loc) )
      b.pack(side='left')
      for bid in bids:
        b=tk.Button(bid_frame,text=bid,font=button_font,command=lambda bid=bid: self.get_bid(order_loc+1,bid,order_loc))
        b.pack(side='left')
        if bid < current_bid+1:
          b['state']=tk.DISABLED
    bid_frame.pack(side='bottom')
    self.hand_frame.pack()
  
  def select_trump(self,winning_bid,winning_bidder_loc):
    winning_bidder_loc=self.order[winning_bidder_loc]

    winning_bidder=self.players[winning_bidder_loc]
    name=winning_bidder.name
    self.hand_frame.destroy()

    dx=self.width/4.
    x_center=self.width/2.
    y_center=self.height/2.

    self.hand_frame=tk.Frame(self.root)

    winning_bidder.show_hand(self.hand_frame)

    suits='Hearts Diamonds Spades Clubs'.split()
    lower_frame=tk.Frame(self.hand_frame)
    for suit in suits:
      b=tk.Button(lower_frame,text=suit,command=lambda suit=suit: self.play_hand(winning_bid,winning_bidder_loc,suit))
      b.pack(side='left')
    lower_frame.pack()
    self.hand_frame.pack()

  def play_hand(self,winning_bid,winning_bidder_loc,trump_suit):
    self.hand_frame.destroy()
    order=[0,1,2,3]
    self.order=order[winning_bidder_loc:]+order[:winning_bidder_loc]

    for loc in self.order:
      player=self.players[loc]
      player.hand.discard(trump_suit)
      num_cards=len(player.hand.cards)
      need=6-num_cards
      if need > 0:
        self.deck.deal(player.hand,need)
      player.hand.sort_hand()

    #for count,loc in enumerate(self.order):
    player=self.players[winning_bidder_loc]
    player.play_card(root,winning_bidder_loc)

      





  def deal(self):
    for i in range(3):
      for loc in self.order:
        player=self.players[loc]
        self.deck.deal(player.hand,3)
    self.get_bid(0,5,0)



scale=0.5
font_size=scale*75
random.seed(1)

root=tk.Tk()
root.title('')

deck=Deck(scale=scale)
deck.shuffle()

players=[
    Pedro_Player('Jacob'),
    Pedro_Player('David'),
    Pedro_Player('Mom'),
    Pedro_Player('Brigette')]
    
game=Pedro_Game(root,deck,players)
game.pick_dealer()

root.mainloop()





#img1 = (Image.open("../deck/01c.png"))
#scale=.75
#font_size=20
#x_center=scale*width/2.
#y_center=scale*height/2.
#dx=scale*width/4.
#for count,img in enumerate(imgs):
#  imgs[count]=ImageTk.PhotoImage(img.resize((int(scale*width),int(scale*height)),Image.ANTIALIAS))
#
#hand_frame=tk.Canvas(root,width=dx*11,
#    height=scale*height)
#for count,img in enumerate(imgs):
#  shift=count*dx
#  hand_frame.create_image(shift+x_center,y_center,image=img)
#hand_frame.pack(anchor=tk.CENTER)
#
#
#
#
#
#
#def func():
#  global hand_frame
#  hand_frame.destroy()
#  global bid_frame
#  bid_frame.destroy()
#  hand_frame=tk.Frame(root,
#      height=scale*height)
#  buttons=[0 for i in range(9)]
#  for count,img in enumerate(imgs):
#    shift=count*dx
#    if count == len(imgs) - 1:
#      buttons[count]=tk.Button(hand_frame,height=scale*height,
#          width=scale*width,image=img,command=lambda count=count: disable(buttons[count]))
#    else:
#      buttons[count]=tk.Button(hand_frame,height=scale*height,
#          width=dx,image=img,command=lambda count=count: disable(buttons[count]))
#    buttons[count].pack(side='left')
#  hand_frame.pack(anchor=tk.CENTER)
#
#b=tk.Button(bid_frame,text='PASS',font=button_font,command=func)
#b.pack(side='left')
#for bid in bids:
#  b=tk.Button(bid_frame,text=bid,font=button_font,command=func)
#  b.pack(side='left')
#  if bid < 8:
#    b['state']=tk.DISABLED
#bid_frame.pack(side='top')
