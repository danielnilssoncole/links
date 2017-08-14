from django.shortcuts import render
from django.shortcuts import get_object_or_404
from links.models import Category, Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context = {'categories': category_list,
               'pages': page_list}
    return render(request, 'links/index.html', context)

def about(request):
    context = {'name': 'daniel'}
    return render(request, 'links/about.html', context)

def show_category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category)
    context = {'category': category,
               'pages': pages}
    return render(request, 'links/category.html', context)
