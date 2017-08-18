from django.shortcuts import render
from django.shortcuts import get_object_or_404
from links.models import Category, Page
from links.forms import CategoryForm

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

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'links/add_category.html', context)

def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context = {'form': form, 'category': category}
    return render(request, 'links/add_page.html', context)
