#!/usr/bin/python
import MySQLdb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--books', dest='books', action='store_true')
parser.add_argument('--reviews', dest='reviews', action='store_true')
parser.add_argument('--categories', dest='categories', action='store_true')
parser.add_argument('--shelves', dest='shelves', action='store_true')
parser.set_defaults(books=False, reviews=False, categories=False, shelves=False)
args = parser.parse_args()

db = MySQLdb.connect(host="mysql.csail.mit.edu",
                     user="test_user",
                     passwd="statacenter",
                     db="bookrecs")
cur = db.cursor()

def insert_data(filename, command, ints=[], floats=[]):
    cur.execute("delete from {0}".format(command.split()[2]))
    cur.commit()
    data = []
    with open(filename) as f:
        for i, row in enumerate(f.readlines()):
            if i > 0 and i % 100 == 0:
                cur.executemany(command, data)
                data = []
            row = row.strip()
            row = row.replace("''","'").replace('"',"'")
            row = row.split('\t')
            for i, val in enumerate(row):
                if i in ints:
                    row[i] = int(val) if val else None
                elif i in floats:
                    row[i] = int(float(val)) if val else None
            row = tuple(row)
            data.append(row)
    cur.executemany(command, data)
    db.commit()

if args.books:
    insert_data('books.tsv', "insert into website_book (book_id, book_title, book_author, book_pub_date, book_publisher, description, pagecount, cover_url) values (%s, %s, %s, %s, %s, %s, %s, %s)", ints=[6])

if args.reviews:
    insert_data('reviews.tsv', 'insert into website_reviews (book_id_id, body, rating, url) values (%s, %s, %s, %s)', floats=[2])

if arg.shelves:
    insert_data('shelves.tsv', 'insert into website_shelves (book_id_id, shelf, people) values (%s, %s, %s)', ints=[2])

if arg.categories:
    insert_data('categories.tsv', 'insert into website_categories (book_id_id, category) values (%s, %s)')

db.close()