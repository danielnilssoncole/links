from django.shortcuts import render
from django.http import HttpResponse
from links.models import Category, Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context = {'categories': category_list}
    return render(request, 'links/index.html', context)

def about(request):
    context = {'name': 'daniel'}
    return render(request, 'links/about.html', context)
