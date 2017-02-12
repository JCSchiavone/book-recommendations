#!/usr/bin/python
import json
import sqlite3
import string
import clean_utils

conn = sqlite3.connect('goodreadsreviews.sqlite')
cur = conn.cursor()

# Setup
cur.executescript('''
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Shelves;

CREATE TABLE Books (
    book_id         INT,
    book_title      TEXT,
    book_author     TEXT,
    book_pub_date   TEXT,
    book_publisher  TEXT,
    description     TEXT,
    pagecount       TEXT,
    UNIQUE(book_title, book_author)
);

CREATE TABLE Reviews (
    book_id               INT,
    body                  TEXT,
    rating                REAL,
    url                   TEXT
);

CREATE TABLE Shelves (
    book_id       INT,
    shelf         TEXT,
    people        TEXT
)
''')

cleanfile = "goodreadsreviews_clean.json"
str_data = open(cleanfile).read()
json_data = json.loads(str_data)

book_id_counter = 0

for entry in json_data:
    try:
        book_title = entry['book_title']
    except:
        book_title = ''

    try:
        book_author = entry['book_author']
    except:
        book_author = ''

    cur.execute("SELECT book_id FROM Books WHERE book_title = ? and book_author = ?", (book_title, book_author))
    id_data = cur.fetchall()
    if len(id_data) == 0:
        book_id = book_id_counter
        book_id_counter += 1
    else:
        book_id = id_data[0][0]

    try:
        if type(entry['body']) == list:
            body = ''
            for paragraph in entry['body']:
                body += paragraph
                body += ' '
        elif type(entry['body']) == str:
            body = entry['body']
        elif type(entry['body']) == unicode:
            body = entry['body']
    except:
        body = ''

    book_pub_date = entry['book_pub_date']
    book_publisher = entry['book_publisher']
    description = None
    pagecount = None
    categories = None
    url = entry['url']

    try:
        rating = entry['rating']
        if not rating:
            rating = None
    except:
        rating = None

    cur.execute('''INSERT INTO Reviews (book_id, body, rating, url)
        VALUES ( ?, ?, ?, ? )''', (book_id, body, rating, url))

    cur.execute('''INSERT OR IGNORE INTO Books (book_id, book_title, book_author, book_pub_date, book_publisher, description, pagecount)
        VALUES ( ?, ?, ?, ?, ?, ?, ? )''', (book_id, book_title, book_author, book_pub_date, book_publisher, description, pagecount))

# add shelf data to new database table
json_file = 'goodreadsshelves.json'
data = []
with open(json_file) as f:
    for line in f:
        if not line.startswith(('[', ']')):
            if line.endswith(',\n'):
                data.append(json.loads(line[:-2]))  # omits comma at end of line
            else:
                data.append(json.loads(line))

shelflist = []
countlist = []
results = []

for item in data:
    newdict = {}
    newdict['book_title'] = item['book_title'][0]
    shelflist = item['shelf']  # list of all the shelf names for that book
    for i, shelf in enumerate(shelflist):  # connects the people counts (as integers) to the correct shelf names as key:value pairs
        peoplecount = item['people'][i]
        newdict[shelf] = int(peoplecount[:-7].replace(',', ''))  # remove commas and " people" at the end of the count
    results.append(newdict)

sel_results = []
valid_chars = set(string.printable)

# remove books with non-English characters in their title, and shelves with non-English characters or less than 5 uses
for book in results:
    if all(letter in valid_chars for letter in book['book_title']):  # only include book if title is all English letters
        # only include shelves that have English names and have more than 5 people using that shelf (but include all book_title key:value pairs (which are unicode))
        sel_book_dict = {key: value for key, value in book.iteritems() if ((type(value) == int and value > 5) or type(value) == unicode) and all(letter in valid_chars for letter in key)}
        sel_results.append(sel_book_dict)

for entry in sel_results:
    book_title = clean_utils.clean_title(entry['book_title'])

    cur.execute("SELECT book_id FROM Books WHERE book_title = ?", (book_title,))
    data_shelf = cur.fetchall()
    if len(data_shelf) == 0:
        print "book title for shelf not found:"
        print book_title
        book_id = None
    else:
        book_id = data_shelf[0][0]

    for key, value in entry.iteritems():
        if not key == 'book_title':
            cur.execute('''INSERT INTO Shelves (book_id, shelf, people)
                VALUES ( ?, ?, ? )''', (book_id, key, value))

conn.commit()
conn.close()
