# Udacity Peter Novig Design of Computer Programs Week 1

#1 define poker function that returns max hand
def poker(hands):
	return max(hands, key=hand_rank)

#8 allmax is to handle ties that can return all hands if multiple hands are all the greatest hand
def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    # Your code here.
    results, maxval = [], None
    key = key or (lambda x:x)
    for item in iterable:
        rank_item = key(item)
        if results == [] or rank_item > maxval:
            results = [item]
            maxval = rank_item
        elif rank_item == maxval:
            results.append(item)
    return results

#2 define a function that can assign rank to each hand
def hand_rank(hand):
	ranks = card_ranks(hand) # assign ranks to each card #
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, kind(2, ranks), kind(2, ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0,  ranks)

#3 return card ranks of list of cards
def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r,s in cards]
    ranks.sort(reverse=True)
    return ranks

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    # Your code here.
    results = {}
    for r in ranks:
        if ranks.count(r) == 2: results.setdefault(r,1)
    if len(results)==2:
        return tuple(sorted(results.keys(), reverse=True))
    else:
        return None

#7 
# Modify the card_ranks(hand) function so that a 
# straight with a low ace (A, 2, 3, 4, 5) will be
# properly identified as a straight by the 
# straight() function.
def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5,4,3,2,1] if ranks == [14,5,4,3,2] else ranks





#4 define straight and flush function to determine whether the cards is straight or flush.
def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    # Your code here.
    if sum(ranks)==(ranks[0]+ranks[-1])*5/2:
        return True
    else:
        return False
    

def flush(hand):
    "Return True if all the cards have the same suit."
    # Your code here.
    suits = [s for r, s in hand]
    if len(set(suits))==1:
        return True
    else:
        return False

#5
def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    # Your code here.
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

#6
def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    # Your code here.
    results = {}
    for r in ranks:
        if ranks.count(r) == 2: results.setdefault(r,1)
    if len(results)==2:
        return tuple(sorted(results.keys(), reverse=True))
    else:
        return None


#9 shuffle cards and deal
import random # this will be a useful library for shuffling

# This builds a deck of 52 cards. If you are unfamiliar
# with this notation, check out Andy's supplemental video
# on list comprehensions (you can find the link in the 
# Instructor Comments box below).

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 

def deal(numhands, n=5, deck=mydeck):
    # Your code here.
    random.shuffle(mydeck)
    return [mydeck[n*i:n*(i+1)] for i in range(numhands)]