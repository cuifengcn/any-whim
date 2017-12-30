# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from models import BlogPost

# Create your views here.
def index(request):
    blog_list = BlogPost.objects.all()
    temp_list = []
    for post in blog_list:
        q = {}
        q['title']     = post.title
        q['timestamp'] = post.timestamp
        q['body']      = map(lambda i:u'\u3000\u3000'+i.strip(),post.body.splitlines())
        temp_list.append(q)
    blog_list = temp_list
    return render(request, 'index.html', locals())
