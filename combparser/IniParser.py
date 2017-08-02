from __future__ import print_function
from __future__ import absolute_import

from combparser import *

#
class IniParser(object):
    def __init__(self):
        super(IniParser,self).__init__()
        
        self.reset()
        
        key_p = re_p(r'\w+')%self.set_key
        val_p = re_p(r'[^\r\n]*')%self.set_val
        cat_p = re_p(r'\w+')%self.set_sec
        
        eq_p  = str_p(':') | str_p('=')
        sec_p = blanks_p >> str_p('[') >> blanks_p >> cat_p >> blanks_p >> str_p(']') >> blanks_p >> eol_p
        ent_p = blanks_p >> key_p >> blanks_p >> eq_p >> blanks_p >> val_p >> blanks_p >> eol_p
        cmt_p = blanks_p >> str_p(';') >> re_p(r'[^\r\n]*') >> eol_p
        nil_p = blanks_p >> eol_p
        
        self.ini_p = star_p(nil_p | cmt_p | sec_p | ent_p)
    
    def reset(self):
        self.curr_sec = ''
        self.curr_key = ''
        self.curr_val = ''
        self.storage = {}
    
    def set_sec(self, _sec, ss):
        sec = _sec[0]
        self.curr_sec = sec
        if sec not in self.storage:
            self.storage[sec] = dict()
        return _sec
    
    def set_key(self, _key, ss):
        key = _key[0]
        self.curr_key = key
        return _key
    
    def set_val(self, _val, ss):
        val = _val[0]
        self.curr_val = val
        self.storage[self.curr_sec][self.curr_key] = self.curr_val
        return _val
    
    def parse_file(self, f):
        if isinstance(f, str):
            with open(f) as ff:
                ss = StringStream(ff.read())
        elif isinstance(f, file):
            ss = StringStream(f.read())
        else:
            raise Exception('Cannot read %s' % f)
        
        self.ini_p.parse(ss, on_good, on_bad)


if __name__ == '__main__':
    from pprint import pprint
    
    ss = StringStream(open('test.ini').read())
    
    p = IniParser()
    p.parse_file('test.ini')
    pprint(p.storage)


