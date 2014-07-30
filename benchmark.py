from __future__ import print_function
import os
import sys
import time

try:
    from html.parser import HTMLParser
    IS_PY3K = True
except ImportError:
    from HTMLParser import HTMLParser
    IS_PY3K = False


HOMEPAGESDIR = 'homepages'
RESULTSDIR = 'results'


class Benchmark(object):

    def __init__(self, handler):
        try:
            files = sorted(os.listdir(HOMEPAGESDIR))
        except OSError as e:
            print(repr(e))
            sys.exit('Run get_pages.py to download the test pages.')
        tot = len(files)
        for n,filename in enumerate(files):
            filename = filename.strip()
            print('%4s/%s %s ' % (n, tot, filename), end='')
            with open(os.path.join(HOMEPAGESDIR, filename), "rb") as f:
                data = f.read()
            try:
                u = data.decode('utf-8')
            except UnicodeDecodeError:
                u = data.decode('iso-8859-1')
            try:
                a = time.time()
                handler.parse(filename, u)
                b = time.time()
                handler.result(filename, b-a, len(data))
            except Exception as e:
                handler.error(filename, e)
            print(' '*80, end='\r')
        print('[%d files parsed]' % tot)
        handler.close()



class BenchmarkHandler(object):

    def __init__(self, strict=None):
        self.strict = strict
        version = sys.version[:6].strip()
        if not os.path.exists(RESULTSDIR):
            print('Creating results dir.')
            os.mkdir(RESULTSDIR)
        fname = "htmlparser_%s%s.tsv" % (version, '_strict' if strict else '')
        self.result_file = open(os.path.join(RESULTSDIR, fname), "w")

    def result(self, hostname, time, size):
        data  = "\t".join([hostname, "%.3f" % time, str(size)])
        #print(data)
        self.result_file.write(data + "\n")

    def error(self, hostname, error):
        data = str(error)
        print(data)
        self.result_file.write(data + "\n")

    def close(self):
        self.result_file.close()


class HTMLParserHandler(BenchmarkHandler):

    def parse(self, hostname, data):
        if self.strict is not None:
            parser = HTMLParser(strict=self.strict) # py3k
        else:
            parser = HTMLParser() # py2
        parser.feed(data)
        parser.close()


if IS_PY3K:
    Benchmark(HTMLParserHandler(strict=True))
    Benchmark(HTMLParserHandler(strict=False))
else:
    Benchmark(HTMLParserHandler())
