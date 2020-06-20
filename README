springer-dl: download the set of books Springer released for free during the
2020 COVID-19 outbreak

- bypasses Google captcha
- supports PDF and EPUB book formats
- sorts by title, includes ISBN in filename
- filtering for categories and titles. The entire set is ~10GB. Be a good citizen.
- no external dependencies

usage: 

```bash
$ python springer_dl.py --help
usage: springer_dl.py [-h] --path PATH [-t FILTER_TITLE] [-c FILTER_CATEGORY]
                      [--pretty] [--dryrun]

springer-dl: download the set of books Springer released for free during the
2020 COVID-19 outbreak

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           path to download books
  -t FILTER_TITLE, --filter-title FILTER_TITLE
                        Keywords to filter category
  -c FILTER_CATEGORY, --filter-category FILTER_CATEGORY
                        Keywords to filter book title
  --pretty              Pretty print the books.
  --dryrun              Print the list of links and titles. Don't download.
```

```bash
$ ls -R books/
'books/Understanding Statistics Using R':
'Understanding Statistics Using R - 978-1-4614-6227-9.epub'
'Understanding Statistics Using R - 978-1-4614-6227-9.pdf'
```


Filter by category and only print the books
```bash
$ python springer_dl.py --path downloads --dryrun -c "computer" --pretty
---------------------------------------
href      : http://link.springer.com/openurl?genre=book&isbn=978-3-662-44874-8
isbn      : 978-3-662-44874-8
category  : Computer Science
title     : Introduction to Evolutionary Computing
---------------------------------------
href      : http://link.springer.com/openurl?genre=book&isbn=978-3-319-13072-9
isbn      : 978-3-319-13072-9
category  : Computer Science
title     : Data Structures and Algorithms with Python
...
```