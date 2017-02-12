"""recommender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from website.views import index, bookrec, search_title, get_recs, check_tags, get_book_info

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^bookrec$', bookrec, name='bookrec'),
    url(r'^search_title$', search_title, name='search_title'),
    url(r'^get_recs', get_recs, name='get_recs'),
    url(r'^check_tags', check_tags, name='check_tags'),
    url(r'^get_book_info', get_book_info, name='get_book_info'),
    
]
