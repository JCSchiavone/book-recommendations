import argparse
import requests
import json
import sys
from bs4 import BeautifulSoup
import urllib
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('database', help='path to sqlite DB containing scraped data.')
args = parser.parse_args()

def load_db(db):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	books = [book for book in c.execute("SELECT * FROM books")]
	reviews = [review for review in c.execute("SELECT * FROM reviews")]
	shelves = [shelf for shelf in c.execute("SELECT * FROM shelves")]
	return [list(book) for book in books], [list(review) for review in reviews], [list(shelf) for shelf in shelves]

def clean_reviews(reviews):
	for r in reviews:
		r[1] = r[1].replace('"',"'").replace('\n',' ').replace('\t',' ')
	return reviews

def get_book_details(books):
	api_key = 'AIzaSyCkKWtDLiIt-tNfq74lWnxIWfkHPquZbpQ'
	api_key_2 = 'AIzaSyAfXz4x8dg6V0zWxPzEsYHK5vSVUUA8vag'
	categories = []
	for i, book in enumerate(books):
		title = book[1]
		author = book[2]
		if i == 499:
			api_key = api_key_2
		js = requests.get('https://www.googleapis.com/books/v1/volumes?q=inauthor:'+author+'+intitle:'+title+'&key=' + api_key).json()
		if js['totalItems'] == 0:
			print "BOOK NOT FOUND - title: {0}, author: {1}".format(title, author)
			book[5] = ""
			book[6] = ""
			continue
		bookid = js["items"][0]["id"]
		book_details = {}
		js = requests.get('https://www.googleapis.com/books/v1/volumes/'+str(bookid)+'?key='+api_key).json()
		if "volumeInfo" in js:
			if "description" in js["volumeInfo"]:
				description = js["volumeInfo"]["description"]
				soup = BeautifulSoup(description, 'html.parser')
				book[5] = soup.get_text().replace('"',"'").replace('\n',' ')
			else:
				book[5] = ""
			if "pageCount" in js["volumeInfo"]:
				book[6] = js["volumeInfo"]["pageCount"]
			else:
				book[6] = ""
			if "categories" in js["volumeInfo"]:
				cats = js["volumeInfo"]["categories"]
				for cat in cats:
					categories.append([i, cat])
	return books, categories

def get_book_images(books, reviews):
	for review in reviews:
		book_id = review[0]
		if len(books[book_id]) < 8:
			books[book_id].append(None)
		if books[book_id][7] == None:
			books[book_id][7] = scrape_image_url(review[3])
	return books

def scrape_image_url(review_url):
	r = urllib.urlopen(review_url).read()
	soup = BeautifulSoup(r, "html.parser")
	div = soup.find_all(class_="leftAlignedImage")[0]
	img = div.find("img")["src"]
	return img

def write_to_files(books, reviews, shelves, categories):
	with open("books.tsv", "wb") as f:
		for book in books:
			book = [val if val != None else "" for val in book]
			line = "\t".join([str(val) if type(val) is int or type(val) is float else val for val in book]) + "\n"
			f.write(line.encode('utf-8'))
	with open("reviews.tsv", "wb") as f:
		for review in reviews:
			review = [val if val != None else "" for val in review]
			line = "\t".join([str(val) if type(val) is int or type(val) is float else val for val in review]) + "\n"
			f.write(line.encode('utf-8'))
	with open("shelves.tsv", "wb") as f:
		for shelf in shelves:
			shelf = [val if val != None else "" for val in shelf]
			line = "\t".join([str(val) if type(val) is int or type(val) is float else val for val in shelf]) + "\n"
			f.write(line.encode('utf-8'))
	with open("categories.tsv", "wb") as f:
		for category in categories:
			category = [val if val != None else "" for val in category]
			line = "\t".join([str(val) if type(val) is int or type(val) is float else val for val in category]) + "\n"
			f.write(line.encode('utf-8'))

books, reviews, shelves = load_db(args.database)
reviews = clean_reviews(reviews)
books, categories = get_book_details(books)
books = get_book_images(books, reviews)
write_to_files(books, reviews, shelves, categories)
