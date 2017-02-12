from django.shortcuts import render
from annoying.decorators import render_to
from django.template.context_processors import request
from django.http.response import JsonResponse

from models import Book


@render_to('website/index.html')
def index(request):
    return {}

@render_to('website/bookrec.html')
def bookrec(request):
    data = request.GET.get('id')
    book = Book.objects.filter(book_id=data)
    return {'book': book}

def search_title(request):
    data = request.POST.get('title')
    
    pos_titles = Book.objects.filter(book_title__icontains=data)
    pos_authors = Book.objects.filter(book_author__icontains=data)
    
    res = []
    
    for book in pos_titles:
        res.append({'title': book.book_title,
                    'author': book.book_author,
                    'cover': book.cover_url,
                    'id': book.book_id})
        
    for book in pos_authors:
        res.append({'title': book.book_title,
                    'author': book.book_author,
                    'cover': book.cover_url,
                    'id': book.book_id})
    
    return JsonResponse({'res': res})