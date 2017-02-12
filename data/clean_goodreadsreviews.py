#!/usr/bin/python
import re
from langdetect import detect
import json
from bs4 import BeautifulSoup


# removes reviews with blank fields and non-english reviews
def trim_reviews(listofjsonreviews):
    output = []
    for review in listofjsonreviews:
        if review['book_title'] and review['body'] and re.search('[a-zA-Z]', review['body']):
            try:
                if detect(review['body']) == 'en':
                    output.append(review)
            except:
                print "could not detect language of " + review['body'] + ", skipped"
    return output


def clean_body(body):
    soup = BeautifulSoup(body, "lxml")
    text = soup.get_text()
    text = text.strip()
    return text


def clean_title(title):
    soup = BeautifulSoup(title, "lxml")
    text = soup.get_text()
    text = re.sub(r'\([^)]*\)', '', text)
    text = text.strip()
    if text.endswith(',') or text.endswith('.'):
        text = text[:-1]
    return text


def clean_byline(byline):
    soup = BeautifulSoup(byline, "lxml")
    text = soup.get_text()
    text = text.replace('"', '')
    text = text.strip()
    if text.endswith('.') or text.endswith(','):
        text = text[:-1]
        text = text.strip()
    if text.startswith('By ') or text.startswith('by '):
        text = text[3:]
    if ' by ' in text:  # remove everything before and including ' by ' (for "Reviewed/Edited/Translated by AA Bastian")
        text = text[(text.find(' by ')+4):]
    return text

infile = "goodreadsreviews.json"
outfile = "goodreadsreviews_clean.json"

# read in data from Goodreads review json
origdata = []
with open(infile, 'r') as datafile:
    origdata = datafile.readlines()
data_gen = (y for y in origdata if y.strip() != '[' and y.strip() != ']' and y)

data = []

for item in data_gen:
    clean = item.strip()
    clean = unicode(clean)
    clean.encode('utf-8')
    if clean.endswith(','):
        clean = clean[:-1]
    data.append(json.loads(clean))

for row in data:
    row['book_title'] = clean_title(row['book_title'][0])

    if row['body']:
        row['body'] = clean_body(row['body'][0])

    if row['rating']:
        soup = BeautifulSoup(row['rating'][0], "lxml")
        cleanrating = soup.get_text()
        if cleanrating == "it was amazing":
            stars = 5
        if cleanrating == "really liked it":
            stars = 4
        if cleanrating == "liked it":
            stars = 3
        if cleanrating == "it was ok":
            stars = 2
        if cleanrating == "did not like it":
            stars = 1
        row['rating'] = stars

    row['book_author'] = clean_byline(row['book_author'][0])

    row['reviewer_name'] = clean_byline(row['reviewer_name'][0])

    if row['book_pub_metadata']:
        # split on 'by'
        metadata = row['book_pub_metadata'][0].split('by ')
        try:
            row['book_pub_date'] = metadata[0].replace('Published', '').strip()
            row['book_publisher'] = metadata[1].strip()
        except:
            row['book_pub_date'] = ''
            row['book_publisher'] = ''
        del row['book_pub_metadata']

    row['review_pub_date'] = row['review_pub_date'][0]

    row['description'] = ''
    row['pagecount'] = ''
    del row['book_genre']
    del row['site']
    del row['review_likes']
    del row['reviewer_bookshelves']

data_trimmed = trim_reviews(data)

with open(outfile, 'w') as target:
    json.dump(data_trimmed, target)
