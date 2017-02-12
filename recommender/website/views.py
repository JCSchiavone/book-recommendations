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
    return {}

def search_title(request):
    data = request.POST.get('title')
    
    pos_titles = Book.objects.filter(book_title__icontains=data)
    pos_authors = Book.objects.filter(book_author__icontains=data)
    
    return JsonResponse({})