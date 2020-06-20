import re
import urllib.request
from html.parser import HTMLParser
from collections import namedtuple

Book = namedtuple("Book", ['href', 'isbn', 'category', 'title'])

def print_book(book):
    print('---------------------------------------')
    for field, value in book._asdict().items():
        print(f"{field:10}: {value}")

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


class GithubParser(Parser):
    '''
    Parser for the source github page.
    https://hnarayanan.github.io/springer-books/

    Gets links, titles, and categories.
    Access Book objects under links attribute. 
    '''

    def __init__(self, links=None):
        super().__init__(links=links)
        self.current_attrs = {}
        self.current_heading = ''
        self.current_title = ''

    def handle_starttag(self, tag, attrs):  
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        if tag == 'a':
            href = self.current_attrs.get('href', '')
            isbn = href.split('isbn=')[1] if 'isbn=' in href else ''
            book = Book(href, isbn, self.current_heading, self.current_title)
            self.links.append(book)

    def handle_data(self, data):
        '''
        Grabs book titles and category headings
        '''
        super().handle_data(data)
        if self.current_tag == 'h2':
            self.current_heading = self.current_attrs.get('id')

        if 'card-title' == self.current_attrs.get('class'):
            title = data.strip()
            if title:
                self.current_title = title

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
