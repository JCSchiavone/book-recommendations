from django.db import models

class Book(models.Model):
    book_id = models.CharField(primary_key=True, max_length=50)
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_pub_date = models.CharField(max_length=40)
    book_publisher = models.CharField(max_length=100)
    description = models.TextField()
    pagecount = models.IntegerField()
    
    def __unicode__(self):
        return self.book_title

class Reviews(models.Model):
    book_id = models.ForeignKey('Book')
    body = models.TextField()
    rating = models.IntegerField()
    url = models.CharField(max_length=100)

class Shelves(models.Model):
    book_id = models.ForeignKey('Book')
    shelf = models.CharField(max_length=200)
    people = models.IntegerField()
    
    def __unicode__(self):
        return self.shelf
    
class Categories(models.Model):
    book_id = models.ForeignKey('Book')
    category = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.category
       
    
    