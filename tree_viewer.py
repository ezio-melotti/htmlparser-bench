# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
try:
    from html.parser import HTMLParser
    from urllib.request import urlopen
    IS_PY3K = True
except ImportError:
    from HTMLParser import HTMLParser
    from urllib import urlopen
    IS_PY3K = False

no_close_tag = [
    'area',
    'base',
    'basefont',
    'br',
    'col',
    'frame',
    'hr',
    'img',
    'input',
    'isindex',
    'link',
    'meta',
    'param',
]

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.indent = 0
        if IS_PY3K:
            super().__init__(strict=False)
        else:
            HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        print('▷'*self.indent, "<%s>" % tag)
        if tag not in no_close_tag:
            self.indent = self.indent + 1
        self.last = tag

    def handle_endtag(self, tag):
        if tag not in no_close_tag:
            self.indent = self.indent - 1
        if self.indent < 0:
            self.indent = 0
        print('◁'*self.indent, "</%s>" % tag)

    def handle_data(self, data):
        data = data.strip().replace('\n', '').replace('\r', '')
        if not data:
            return
        datalen = len(data)
        if datalen > 30:
            print('▶'*self.indent, data[:30], datalen)
        else:
            print('▶'*self.indent, data)

for page in sys.argv[1:]:
    print('='*80)
    print('Parsing', page)
    print('='*80)
    parser = MyHTMLParser()
    if page.startswith('http://'):
        data = urlopen(page).read()
    else:
        with open(page, "rb") as f:
            data = f.read()
    try:
        u = data.decode('utf-8')
    except UnicodeDecodeError:
        u = data.decode('iso-8859-1')
    #for c in u:
    #    parser.feed(c)
    parser.feed(u)
