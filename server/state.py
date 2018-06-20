
import cgi

import cgitb
cgitb.enable()

import os
import urllib.parse


print('Content-Type: text/html')
print()

print('<title>State</title>')
print('<h1>State</h1>')
print('<p>Hello</p>')

name = None

env = os.environ
if 'QUERY_STRING' in env:
    qstr = env['QUERY_STRING']
    qdict = urllib.parse.parse_qs(qstr)
    if 'name' in qdict:
        name = qdict['name'][0]

print("<p><strong>%s</strong></p>" % (name if name else '...'))




