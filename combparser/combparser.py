from __future__ import print_function

import re

#
class EOSException(Exception):
    pass

class ParserException(Exception):
    pass

#
class StringStream(object):
    def __init__(self, s, begin=0):
        self.s = s
        self.pos = begin
        self.end = len(s)
    
    def peek(self, n=1):
        if self.eos():
            return None
        else:
            return self.s[self.pos:self.pos+n]
    
    def peekall(self):
        return self.peek(self.end-self.pos)
    
    def eos(self):
        return self.pos >= self.end
    
    def move(self, n):
        self.pos += n
    
    
    def __str__(self):
        return 'Stream[%d:]: %s' % (self.pos, self.s[ss.pos:])
    
#
class ParserBase(object):
    
    def __init__(self):
        self.on_action = None
        # self. = self.on_bad
    
    def __mod__(self, action):
        self.on_action = action
        return self
        
    def on_error(self, msg, ss):
        print('On error, %s' % ss)
        raise ParserException(msg)
    
    pass


#
class LiteralP(ParserBase):
    def __init__(self, s):
        super(LiteralP,self).__init__()
        self.s = s
    
    def parse(self, ss, good, bad):
        # print("Parse literal %s from Stream %s" % (self.s, ss))
        
        if ss.eos():
            return bad('End of stream', ss)
        
        nn = len(self.s)
        res = ss.peek(nn)
        if self.s != res:
            return bad('Literal %s expected, %s found' % (self.s, res), ss)
        
        # move forward
        ss.move(nn)
        
        res = [res]
        
        if self.on_action != None:
            res = self.on_action(res, ss)
        
        return good(res, ss)
    
    def __str__(self):
        return 'Literal %s' % (self.s)

# 
class RegexP(ParserBase):
    def __init__(self, regex):
        super(RegexP, self).__init__()
        self.regex = regex
        self.prog = re.compile(regex)
        
    def parse(self, ss, good, bad):
        if ss.eos():
            return bad('End of stream', ss)
        
        # TODO 
        sall = ss.peekall()
        match = self.prog.match(sall)
        if not match:
            return bad('Regex %s not match' % (self.regex,), ss)
        
        res = match.group()
        ss.move(len(res))
        
        res = [res]
        
        if self.on_action != None:
            res = self.on_action(res, ss)
        
        return good(res, ss)

    def __str__(self):
        return "Regex %s" % (self.regex)

#
class SeqP(ParserBase):
    def __init__(self, p1, p2):
        super(SeqP, self).__init__()
        self.x = p1
        self.y = p2
    
    def parse(self, ss, good, bad):
        
        results = []
        
        def gg(res, sstream):
            # results.append(res)
            results.extend(res)
            rr = results
            if self.on_action:
                rr = self.on_action(results, sstream)
            return good(rr, sstream)
        
        def cont(res, sstream):
            # results.append(res)
            results.extend(res)
            return self.y.parse(sstream, gg, bad)
            
        return self.x.parse(ss, cont, bad)
    
    def __str__(self):
        return "Seq(%s,%s)" % (self.x,self.y)

#
class TreeP(ParserBase):
    def __init__(self, p1, p2):
        super(SeqP, self).__init__()
        self.x = p1
        self.y = p2
    
    def parse(self, ss, good, bad):
        
        results = []
        
        def gg(res, sstream):
            results.append(res)
            # results.extend(res)
            if self.on_action:
                self.on_action(results, sstream)
            return good(results, sstream)
        
        def cont(res, sstream):
            results.append(res)
            # results.extend(res)
            return self.y.parse(sstream, gg, bad)
            
        return self.x.parse(ss, cont, bad)
    
    def __str__(self):
        return "Seq(%s,%s)" % (self.x,self.y)
#
class OrP(ParserBase):
    def __init__(self, p1, p2):
        super(OrP,self).__init__()
        self.x = p1
        self.y = p2
        
    def parse(self, ss, good, bad):
        
        def gg(res, sstream):
            if self.on_action:
                self.on_action(res, sstream)
            return good(res, sstream)
        
        def bb(msg, sstream):
            return self.y.parse(sstream, gg, bad)
        
        return self.x.parse(ss, gg, bb)

#
class ManyP(ParserBase):
    def __init__(self, p):
        super(ManyP,self).__init__()
        self.x = p
    
    def parse(self, ss, good, bad):
        
        results = []
        
        def gg(res, sstream):
            results.extend(res)
            # results.append(res)
            return True
        def bb(msg, sstream):
            return False
        
        while self.x.parse(ss, gg, bb):
            pass
        
        if self.on_action:
            self.on_action(result, ss)
        
        return good(results, ss)


#
class WrapParser(ParserBase):
    '''Wrap a true parser.
    It helps us define recursive parsers.
    You may uses it as follows:
    >>> awrap.p = real_p | bwrap
    >>> bwrap.p = lpar_p >> awrap >> rpar_p
    Therefore, the keypoint is to avoid using exact wrap.p but wrap itself.
    '''
    
    def __init__(self, p=None):
        super(WrapParser,self).__init__()
        self.p = p
    
    def parse(self, ss, good, bad):
        return self.p.parse(ss, good, bad)


####



def str_p(s):
    return LiteralP(s)

def re_p(s):
    return RegexP(s)

def star_p(p):
    return ManyP(p)

def plus_p(p):
    return (p >> ManyP(p))

# define some useful parsers
# they can be used directly

lpar_p      = str_p('(')
rpar_p      = str_p(')')
lbrack_p    = str_p('[')
rbrack_p    = str_p(']')

eol_p       = re_p(r'\r?\n')
w_p         = re_p(r'\w')
alnum_p     = re_p(r'[0-9a-zA-Z]')
blank_p     = re_p(r'[ \t]')
num_p       = re_p(r'[0-9]')


# define the ()* version
# ws_p        = re_p(r'\w*')
blanks_p    = re_p(r'[ \t]*')

####
def on_good(s, ss):
    # return s
    # print(s)
    return s

def on_bad(msg, ss):
    print('Stream[%d:]: %s' % (ss.pos,ss.s[ss.pos:]))
    raise ParserException(msg)

def action_print(s, ss):
    print("Result: %s" % s)
    return 
####

def make_seq(x, y):
    return SeqP(x, y)

# def make_tree(x, y):
    # return TreeP(x, y)
    
def make_or(x, y):
    return OrP(x,y)

def make_many(x):
    return ManyP(x)

# bind operators
ParserBase.__rshift__ = make_seq
ParserBase.__or__ = make_or
# ParserBase.__add__ = make_tree
 

if __name__ == '__main__':
    ss = StringStream('homuhoge')
    
    # print(str_p('h').parse(ss, on_good, on_bad))
    # print(str_p('o').parse(ss, on_good, on_bad))
    # print(str_p('m').parse(ss, on_good, on_bad))
    # print(str_p('u').parse(ss, on_good, on_bad))
    # print(str_p('z').parse(ss, on_good, on_bad))
    
    # pp =  str_p('homu') >> str_p('ho') >> str_p('ge')
    # pp =  str_p('ho') >> str_p('mu') >> str_p('ho') >> str_p('ge')
    pp =  str_p('homu')%action_print >> (str_p('ho') >> str_p('g'))%action_print >> str_p('e')
    # print(pp)
    # pp =  str_p('homu')%action_print >> (str_p('ge') | str_p('ho'))%action_print
    # pp =  str_p('homu') >> (str_p('ge') | str_p('ho')) >> (str_p('ge') | str_p('ho'))
    # pp =  str_p('homu')%action_print >> re_p(r'\w*')%action_print
    
    pp = pp%action_print
    pp.parse(ss, on_good, on_bad)
    
    


