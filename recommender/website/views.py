from django.shortcuts import render
from annoying.decorators import render_to
from django.template.context_processors import request
from django.http.response import JsonResponse

from models import Book, Shelves, Categories

@render_to('website/index.html')
def index(request):
    data = request.GET.get('search')
    if data:
        return {'search': data}
    else:
        return {'search': ''}

@render_to('website/bookrec.html')
def bookrec(request):
    data = request.GET.get('id')
    book = Book.objects.get(book_id=data)
    
    tags = Shelves.objects.filter(book_id=data).order_by('-people')
    cats = Categories.objects.filter(book_id=data)
    
    return {'book': book,
            'tags': tags,
            'cats': cats}

def get_recs(request):
    tags_get = request.POST.get('tags')
    if tags_get:
        tags_get = tags_get.split(',')
    id = request.POST.get('id')
    print tags_get
    print id
    other_tags = Shelves.objects.filter(shelf__in=tags_get).select_related()
    res = {}
    for tag in other_tags:
        if tag:
            book = tag.book_id
            if book.book_id != id:
                if book.book_id in res:
                    res[book.book_id]['count'] += 1
                else:
                    res[book.book_id] = {'title': book.book_title,
                                    'author': book.book_author,
                                    'cover': book.cover_url,
                                    'id': book.book_id,
                                    'count': 1
                                    }
    other_cats = Categories.objects.filter(category=tags_get).select_related()
    for tag in other_cats:
        book = tag.book_id
        if book.book_id != id:
            if book.book_id in res:
                res[book.book_id]['count'] += 1
            else:
                res[book.book_id] = {'title': book.book_title,
                                'author': book.book_author,
                                'cover': book.cover_url,
                                'id': book.book_id,
                                'count': 1
                                }
    json_res = []
    for item, val in sorted(res.items(), key=lambda x: x[1]['count'], reverse=True):
        json_res.append(val)
    
    
    return JsonResponse({'res': json_res})
    

def search_title(request):
    data = request.POST.get('title')
    res = search(data)
    
    return JsonResponse({'res': res})

def search(data):
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
    return res
    