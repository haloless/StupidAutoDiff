from __future__ import print_function
from __future__ import absolute_import

from combparser import *




#
class ExprParser(object):
    '''Parser for simple arithmetic expressions.
    Support +-*/()
    '''
    
    def __init__(self):
        super(ExprParser,self).__init__()
        self.reset()
        
        int_p = re_p(r'[0-9]+')
        
        # factor_p = int_p%self.on_val | (str_p('-') >> int_p)%self.on_neg
        
        # mul_p = (factor_p >> str_p('*') >> factor_p) % self.on_mul
        # div_p = (factor_p >> str_p('*') >> factor_p) % self.on_div
        
        # term_p = mul_p | div_p
        # add_p = (term_p >> str_p('+') >> term_p) % self.on_add
        # sub_p = (term_p >> str_p('-') >> term_p) % self.on_sub
        
        # expr_p = add_p | sub_p
        
        
        fact_p = WrapParser()
        term_p = WrapParser()
        expr_p = WrapParser()
        
        fact_p.p = int_p%self.on_val | (str_p('-') >> fact_p)%self.on_neg | (lpar_p >> expr_p >> rpar_p)%self.on_par
        term_p.p = (fact_p >> star_p(re_p(r'[*/]') >> fact_p))%self.on_muldiv
        expr_p.p = (term_p >> star_p(re_p(r'[+\-]')>> term_p))%self.on_addsub
        
        # 
        self.p = star_p(expr_p)
        
    def reset(self):
        self.lval = 0
        self.rval = 0
        
    def parse_str(self, s):
        ss = StringStream(s)
        self.p.parse(ss, self.on_finish, on_bad)
        
    def on_val(self, res, ss):
        print('val: %s' % res)
        a = self.cast_val(res[0])
        return [a]
    
    def on_par(self, res, ss):
        print('par: %s' % res)
        return res[1:-1]
    
    def on_muldiv(self, res, ss):
        print('muldiv: %s' % res)
        a = self.cast_val(res[0])
        for i in range(1,len(res),2):
            op = res[i]
            b = self.cast_val(res[i+1])
            a = a*b if op=='*' else a/b
        return [a]
    def on_addsub(self, res, ss):
        print('addsub: %s' % res)
        a = self.cast_val(res[0])
        for i in range(1,len(res),2):
            op = res[i]
            b = self.cast_val(res[i+1])
            a = a+b if op=='+' else a-b
        return [a]
    
    def on_mul(self, res, ss):
        print('mul: %s' % res)
        a,b = self.cast_binary(res)
        c = a * b
        return [c]
        
    def on_div(self, res, ss):
        print('div: %s' % res)
        a,b = self.cast_binary(res)
        c = a / b
        return [c]
        
    def on_add(self, res, ss):
        print('add: %s' % res)
        a,b = self.cast_binary(res)
        c = a + b
        return [c]
        
    def on_sub(self, res, ss):
        print('sub: %s' % res)
        a,b = self.cast_binary(res)
        c = a - b
        return [c]
        
    def on_neg(self, res, ss):
        print('neg: %s' % res)
        a = self.cast_unary(res)
        c = -a
        return [c]
    
    def on_finish(self, res, ss):
        print('Result = %s' % res)
        return res
    
    def cast_binary(self, res):
        return self.cast_val(res[0]),self.cast_val(res[2])
    def cast_unary(self, res):
        return self.cast_val(res[1])
    def cast_val(self, s):
        return int(s)
    

#
if __name__ == '__main__':
    # expr_s = '(11+22)*(33+44)-6/(-2)'
    # expr_s = '(11+22+33+44)-6/(-2)'
    expr_s = '1*2+3*4+4*5+5*6'
    # expr_s = '3*2+1*-1'
    
    p = ExprParser()
    p.parse_str(expr_s)
    
    
    
    
    
    
    
    


