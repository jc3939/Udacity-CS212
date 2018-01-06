#1
def search(pattern, text):
    """Return true if pattern appears anywhere in text
	   Please fill in the match(          , text) below.
	   For example, match(your_code_here, text)"""
    if pattern.startswith('^'):
        return match( pattern[1:]             , text) # fill this line
    else:
        return match( '.*'+pattern            , text) # fill this line

#2
def match(pattern, text):
    """
    Return True if pattern appears at the start of text
    
    For this quiz, please fill in the return values for:
        1) if pattern == '':
       	2) elif pattern == '$':
	"""

    if pattern == '':
        return True
    elif pattern == '$':
        return text==''

    #3 this action requires us to write function match_star and match1
    elif len(pattern) > 1 and pattern[1] in '*?':
        p, op, pat = pattern[0], pattern[1], pattern[2:]
        if op == '*':
            return match_star(p, pat, text)
        elif op == '?':
            if match1(p, text) and match(pat, text[1:]):
                return True
            else:
                return match(pat, text)
    else:
        return (match1(pattern[0], text) and
                match(pattern[1:],text )) # fill in this line

def match1(p, text):
	"""return true if first character of text matches pattern character p."""
	if not text: return False
	return p=='.' or p==text[0]

def match_star(p, pattern, text):
	"""return true if any number of character p followed by pattern, matches text"""
	return (match(pattern, text) or (match1(p, text) and match_star(p, pattern, text[1::])))

null = frozenset()
#4
def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y

#return set of REMAINDERS
def matchset(pattern, text):
    "Match pattern at start of text; return a set of remainders of text."
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
    elif 'dot' == op:
        #print 
        return set([text[1:]]) if text else null
    elif 'oneof' == op:
        return set([text[1:]]) if text[0] in x else null
    elif 'eol' == op:
        return set(['']) if text == '' else null
    elif 'star' == op:
        return (set([text]) |
                set(t2 for t1 in matchset(x, text)
                    for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)

def test():
    assert matchset(('lit', 'abc'), 'abcdef')            == set(['def'])
    assert matchset(('seq', ('lit', 'hi '),
                     ('lit', 'there ')), 
                   'hi there nice to meet you')          == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'), 
                    ('lit', 'cat')), 'dog and cat')      == set([' and cat'])
    assert matchset(('dot',), 'am i missing something?') == set(['m i missing something?'])
    assert matchset(('oneof', 'a'), 'aabc123')           == set(['abc123'])
    assert matchset(('eol',),'')                         == set([''])
    assert matchset(('eol',),'not end of line')          == frozenset([])
    assert matchset(('star', ('lit', 'hey')), 'heyhey!') == set(['!', 'heyhey!', 'hey!'])
    
    return 'tests pass'

#5 
# Fill out the API by completing the entries for alt, 
# star, plus, and eol.
# the problem of matchset function there is an inherent inefficiency that we need to define
# patterns many times, thus we need compiler function which avoid repetition.
def lit(string):  return ('lit', string)
def seq(x, y):    return ('seq', x, y)
def alt(x, y):    return ('alt', x, y)
def star(x):      return ('star', x)
def plus(x):      return seq(x, star(x))
def opt(x):       return alt(lit(''), x) #opt(x) means that x is optional
def oneof(chars): return ('oneof', tuple(chars))
dot = ('dot',)
eol = ('eol',)

def test():
    assert lit('abc')         == ('lit', 'abc')
    assert seq(('lit', 'a'), 
               ('lit', 'b'))  == ('seq', ('lit', 'a'), ('lit', 'b'))
    assert alt(('lit', 'a'), 
               ('lit', 'b'))  == ('alt', ('lit', 'a'), ('lit', 'b'))
    assert star(('lit', 'a')) == ('star', ('lit', 'a'))
    assert plus(('lit', 'c')) == ('seq', ('lit', 'c'), 
                                  ('star', ('lit', 'c')))
    assert opt(('lit', 'x'))  == ('alt', ('lit', ''), ('lit', 'x'))
    assert oneof('abc')       == ('oneof', ('a', 'b', 'c'))
    return 'tests pass'
#6 define search and match function,
# search function returns text where pattern find a match in ANY part of text
# match function returns text where pattern find a match in BEGINNING part of text
def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m:
            return m
        
def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = matchset(pattern, text)
    #8 
    # Fill out the function match(pattern, text), so that 
	# remainders is properly assigned. 
    remainders = pattern(text)

    if remainders:
        shortest = min(remainders, key=len)
        return text[:(len(text)-len(shortest))]

def test():
    assert match(('star', ('lit', 'a')),'aaabcd') == 'aaa'
    assert match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == None
    assert match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'
    assert search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'
    return 'tests pass'
#7
# Write the compiler for alt(x, y) in the same way that we 
# wrote the compiler for lit(s) and seq(x, y). 

def lit(s): return lambda text: set([text[len(s):]]) if text.startswith(s) else null

def seq(x, y): return lambda text: set().union(*map(y, x(text)))

def alt(x, y): return lambda text: x(text) | y(text)

def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null
dot = lambda t: set([t[1:]]) if t else null
eol = lambda t: set(['']) if t == '' else null
def star(x): return lambda t: (set([t]) | 
                               set(t2 for t1 in x(t) if t1 != t
                                   for t2 in star(x)(t1)))


#9
# Complete the code for the compiler by completing the constructor
# for the patterns alt(x, y) and oneof(chars). 
# You can move set([s]) to left side to avoid repetition since s is not dependent of Ns
def lit(s):
	##You can move set([s]) to left side to avoid repetition since s is not dependent of Ns
	##set_s = set([s])         
	return lambda Ns: set([s]) if len(s) in Ns else null
def alt(x, y):      return lambda Ns: x(Ns) | y(Ns)
def star(x):        return lambda Ns: opt(plus(x))(Ns)
def plus(x):        return lambda Ns: genseq(x, star(x), Ns, startx=1) #Tricky
def oneof(chars):   return lambda Ns: set(chars) if 1 in Ns else null
def seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def opt(x):         return alt(epsilon, x)
dot = oneof('?')    # You could expand the alphabet to more chars.
epsilon = lit('')   # The pattern that matches the empty string.


null = frozenset([])

def test():
    
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null 
    
    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])
    
    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null
    
    return 'tests pass'


# initial definition of genseq
# It returns correct values but not always return bc it falls to infinit loop
# when plus(opt(a)) where a= lit('a') and opt(a) returns empty string
def genseq(x, y, Ns):
	Nss = range(max(Ns)+1)
	return set(m1+m2 for m1 in x(Nss) for m2 in y(Nss) if len(m1+m2) in Ns)

# new definition of genseq
def genseq(x, y, Ns, startx=0):
	#set of matches to xy whose total len is in Ns, with x-match's len in Ns_x
	#Tricky part: x+ is defined as x+ =x x*
	#To stop recursion, the first x must generate at least 1 char
	#and then the recursive x* has that many fewer characters. We use
	# startx=1 to say that x must match at least 1 character
	if not Ns:
		return null
	xmatches = x(set(range(startx, max(Ns)+1)))
	Ns_x = set(len(m) for m in xmatches)
	Ns_y = set(n-m for n in Ns for m in Ns_x if n-m>=0)
	ymatches = y(Ns_y)
	return set(m1+m2 for m1 in xmatches for m2 in ymatches if len(m1+m2) in Ns)



# Write a function, n_ary(f), that takes a binary function (a function
# that takes 2 inputs) as input and returns an n_ary function. 
from functools import update_wrapper
def decorator(d):
	"Make function d a decorator: d wraps a function fn"
	def _d(fn):
		return update_wrapper(d(fn),fn)
	update_wrapper(_d,d)
	return _d


@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        # your code here
        if len(args)==0:
            return x
        elif len(args)==1:
            return f(x, args[0])
        else:
            return f(x, n_ary_f(*args))
    return n_ary_f

@n_ary
def seq(x,y): return ('seq', x, y)



@decorator
def memo(f):
	cache = {}
	def _f(*args):
		try:
			return cache[args]
		except KeyError:
			cache[args] = result = f(*args)
		except TypeError:
			# some element of args cannot be dict key
			return f(args)
	return _f