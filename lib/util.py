import re
import urllib.request
from html.parser import HTMLParser

class Parser(HTMLParser):
    def __init__(self, links=None):
        HTMLParser.__init__(self)
        if links is None:
            self.links = []
        else:
            self.links = links
        self.title = []
        self.current_tag = None
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'a':
            self.links.append(dict(attrs).get('href'))
    def handle_data(self, data):
        if self.current_tag == 'title':
            self.title.append(data)

def request(url, headers):
    conn = urllib.request.Request(
        url,
        headers=headers
    )
    r = urllib.request.urlopen(conn)
    return r

def download_file(url, headers, dest):
    BLOCK = 16 * 1024
    conn = urllib.request.Request(
        url,
        headers=headers
    )
    resp = urllib.request.urlopen(conn)
    with open(dest, 'wb') as f:
        while True:
            chunk = resp.read(BLOCK)
            if not chunk:
                break
            f.write(chunk)
