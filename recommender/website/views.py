from django.shortcuts import render
from annoying.decorators import render_to



@render_to('website/index.html')
def index(request):
    return {}

@render_to('website/bookrec.html')
def bookrec(request):
    return {}