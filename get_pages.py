import os
import os.path
import socket
from urllib.request import urlretrieve
socket.setdefaulttimeout(8)


# This should download pages in parallel.
# Currently it might take over half an hour to download 1000 pages.

HOMEPAGESDIR = 'homepages'

def get_pages(limit=1000):
    if not os.path.exists(HOMEPAGESDIR):
        print('Creating homepages dir.')
        os.mkdir(HOMEPAGESDIR)
    with open('sites100k.txt') as sites:
        for n,site in enumerate(sites):
            if n > limit:
                break
            site = site.strip()
            try:
                print('[%4d/%d]' % (n, limit), site.ljust(30), end=' ')
                path = os.path.join(HOMEPAGESDIR, site)
                if not os.path.exists(path):
                    urlretrieve('http://'+site, path)
                    print('[done]')
                else:
                    print('[already downloaded]')
            except Exception as e:
                print('[%r]' % e)

if __name__ == '__main__':
    get_pages()
