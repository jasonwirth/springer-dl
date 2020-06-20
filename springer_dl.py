#!/usr/bin/env python3

import argparse
import os
import sys
import urllib.parse
from lib.util import GithubParser, Parser, request, download_file, print_book

if __name__ == '__main__':
    desc = 'springer-dl: download the set of books Springer released for free '\
           'during the 2020 COVID-19 outbreak'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--path', dest='path', type=str,
                        help='path to download books', required=True)
    parser.add_argument('-t', '--filter-title', help="Keywords to filter category")
    parser.add_argument('-c', '--filter-category', help="Keywords to filter book title")
    parser.add_argument('--pretty', action='store_true', help="Pretty print the books.")
    parser.add_argument('--dryrun', default=False, action="store_true",
                        help="Print the list of links and titles. Don't download.")
    args = parser.parse_args()

    dl_path = args.path
    os.makedirs(dl_path, exist_ok=True)

    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like '\
               'Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '\
               'CriOS/81.0.4044.124 Mobile/15E148 Safari/604.1'}
    BOOK_PAGE = "https://hnarayanan.github.io/springer-books/"

    r = request(BOOK_PAGE, headers=HEADERS)
    html = r.read().decode('utf-8')

    p = GithubParser()
    p.feed(html)

    prefix = 'http://link.springer.com/openurl'
    books = [book for book in p.links if book.href.startswith(prefix)]

    if args.filter_title:
        text = args.filter_title.lower()
        books = [b for b in books if text in b.title.lower()]
    
    if args.filter_category:
        text = args.filter_category.lower()
        books = [b for b in books if text in b.category.lower()]        

    if args.dryrun:
        for b in books:
            if args.pretty:
                print_book(b)
            else:
                print(b)
        sys.exit()

    for url, isbn, category, title in books:
        r = request(url, HEADERS)
        end_url = r.url

        html = r.read().decode('utf-8')
        p = Parser()
        p.feed(html)

        links = [x for x in p.links if 'content/pdf' in x or 'download/epub' in x]
        links = [urllib.parse.urljoin(end_url, x) + '?javascript-disabled=true' for x in links]

        book_title = p.title[0].split(' |')[0]
        book_path = os.path.join(dl_path, book_title)
        os.makedirs(book_path, exist_ok=True)

        if 'epub' in links[1]:
            links = links[:2]
        else:
            links = links[:1]

        for link in links:
            filename = '%s - %s' % (book_title, isbn) + os.path.splitext(
                urllib.parse.urlparse(link).path)[-1]
            filepath = os.path.join(book_path, filename)
            if os.path.exists(filepath):
                continue
            try:
                print('[+] %s' % filename)
                download_file(link, HEADERS, filepath)
            except KeyboardInterrupt:
                if os.path.exists(filepath):
                    os.remove(filepath)
                sys.exit()
            except:
                print('[x] error downloading %s, skipping...' % filename)
