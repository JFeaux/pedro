#!/usr/bin/python

import sys
from random import shuffle,seed
from itertools import product

class Card:
  FACES = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
  SUITS={'Hearts':1,'Diamonds':2,'Spades':3,'Clubs':4}
  COLORS={'Hearts':0,'Diamonds':0,'Spades':1,'Clubs':1}

  def __init__(self, rank, suit):
    self.suit = suit
    self.rank = rank

    self.suit_rank=self.SUITS[suit]
    self.sort_rank=self.rank
    if rank == 5:
      if self.suit_rank == 1 or self.suit_rank == 3:
        self.sort_rank=100
      else:
        self.sort_rank=0

  def __str__(self):
    value = self.FACES.get(self.rank, self.rank)
    return "{0} of {1}".format(value, self.suit)

  def __repr__(self):
    return str(self)

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


class Deck:

  def __init__(self):
    ranks=range(2,15)
    suits='Spades Diamonds Clubs Hearts'.split()
    self.cards=[Card(r,s) for s,r in product(suits,ranks)]

  def __str__(self):
    s=''
    for i in range(len(self.cards)):
      s=s + ' ' * i + str(self.cards[i]) + '\n'
    return s

  def __repr__(self):
    pass


  def shuffle(self):
    shuffle(self.cards)

  def deal(self,hand,num_cards=1):
    for i in range(num_cards):
      hand.add(self.cards.pop())

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

class Pedro_game:
  def __init__(self,players):
    self.players=players
    self.trump_suit=None

  def deal_round(self,first_bidder):
    self.deck=Deck()
    self.deck.shuffle()
    order=[i for i in range(first_bidder,4)]+[i for i in range(first_bidder)]
    for player in self.players:
      player.clear_hand()
    for i in range(3):
      for j in order:
        self.deck.deal(self.players[j],3)
    for i in order:
      self.players[i].sort_hand()

  def bidding(self,first_bidder):
    current_bid=5
    winning_bidder=-1
    order=[i for i in range(first_bidder,4)]+[i for i in range(first_bidder)]
    for i,j in enumerate(order):
      print self.players[j]
      if current_bid < 14:
        bid=int(raw_input('Bid?\n'))
        if bid > current_bid:
          current_bid=bid
          winning_bidder=j
      else:
        bid=int(raw_input('Bid?\n'))
        if bid == 14 and i == 3:
          current_bid=bid
          winning_bidder=j
    print current_bid
    print winning_bidder
    self.winning_bidder=winning_bidder
    print self.players[winning_bidder]
    self.trump_suit=raw_input('Trump suit?\n')

  def second_deal(self,first_bidder):
    order=[i for i in range(first_bidder,4)]+[i for i in range(first_bidder)]
    for i,j in enumerate(order):
      self.players[j].discard(self.trump_suit)
      take=6-len(self.players[j].cards)
      if take > 0:
        self.deck.deal(self.players[j],take)
      self.players[j].sort_hand()

  def play_trick(self,lead):
    trick=Trick(self.trump_suit)
    order=[i for i in range(lead,4)]+[i for i in range(lead)]
    for i,j in enumerate(order):
      print self.players[j]
      card_number=int(raw_input('Play Card?\n'))
      card=self.players[j].play(card_number)
      trick.add(card)
      print trick

class Trick:
  def __init__(self,trump_suit,lead_card):
    self.cards=[lead_card]
    self.trump_suit=trump_suit

  def add(self,card):
    self.cards.append(card)

  def __str__(self):
    s=''
    for i in range(len(self.cards)):
      s=s + ' '+str(i+1)+':'+' ' * (i+1) + str(self.cards[i]) + '\n'
    return s

  def __repr__(self):
    return str(self)


class Pedro_Player(object):
  def __init__(self,name):
    self.name=name
    self.hand=Hand()
    
  def bid(self,min_bid):
    if min_bid > 14:
      return False
    else:
      if min_bid > 5:
        ask='Current Bid: '+min_bid-1+'\n'
      else:
        ask='Minimum Bid: 6\n'
      ask+='  '+self.name+': Bid?\n'
      invalid_bid=True
      while invalid_bid:
        try:
          bid=int(raw_input(ask))
          if bid > min_bid and bid < 14:
            return bid
          else:
            msg='Must be greater than '+str(min_bid)
            msg+=' and less than 14'
            print msg
        except ValueError:
          print 'Please insert integer'

  def discard(self,trump):
    pass

  def play_card(self,card):
    pass

class Dealer(Pedro_Player):
  def __init__(self,pedro_player):
    """ 
    Dealer classes intialized 
    by a Pedro_Player instance 
    """
    self.name=pedro_player.name
    self.hand=pedro_player.hand

  def bid(self,current_bid):
    return bid

jacob=Pedro_Player('Jacob')
jacob.bid(5)

sys.exit()


# to do dealer rotation
players=['a','b','c','d']
print players
dealer=players.pop()
players.insert(0,dealer)
print players


  





seed(1)

# initialize the players
#Jacob=Hand('Jacob')
#Brigette=Hand('Brigette')
#David=Hand('David')
#Richard=Hand('Richard')
#
#players=[Jacob,Brigette,David,Richard]
#game=Pedro_game(players)
#game.deal_round(0)
#game.bidding(0)
#game.second_deal(0)
#game.play_trick(game.winning_bidder)
#




