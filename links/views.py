from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from links.webhose_search import run_query
from links.models import Category, Page, UserProfile
from django.contrib.auth.models import User
from links.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context = {'categories': category_list,
               'pages': page_list}
    visitor_cookie_handler(request)
    context['visits'] = request.session['visits']
    response = render(request, 'links/index.html', context)
    return response

def about(request):
    context = {'name': 'daniel'}
    return render(request, 'links/about.html', context)

def show_category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category).order_by('-views')
    context = {'category': category,
               'pages': pages}
    context['query'] = category.name
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context['query'] = query
            context['result_list'] = result_list
    return render(request, 'links/category.html', context)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('links:index'))
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'links/add_category.html', context)

@login_required
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
                return HttpResponseRedirect(reverse('links:show_category', args=(category_name_slug,)))
        else:
            print(form.errors)
    context = {'form': form, 'category': category}
    return render(request, 'links/add_page.html', context)

@login_required
def restricted(request):
    return HttpResponse('Since you\'re logged in, you can see this text!')


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def search(request):
    result_list = []
    query = ''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
    context = {
        'result_list' : result_list,
        'query' : query
        }
    return render(request, 'links/search.html', context)

def track_url(request):
    page_id = None
    url = '/links/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)

def track_cat(request):
    cat_slug = None
    url = '/links/'
    if request.method == 'GET':
        if 'cat_slug' in request.GET:
            cat_slug = request.GET['cat_slug']
            try:
                cat = Category.objects.get(slug=cat_slug)
                cat.views += 1
                cat.save()
                url = '/links/category/{0}'.format(cat_slug)
            except:
                pass
    return redirect(url)

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return HttpResponseRedirect(reverse('links:index'))
        else:
            print(form.errors)
    context = {'form' : form}
    return render(request, 'links/profile_registration.html', context)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('links:index')
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({
        'website' : userprofile.website,
        'picture' : userprofile.picture
    })
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('links:profile', args=(user.username,)))
        else:
            print(form.errors)
    context = {
        'userprofile' : userprofile,
        'selecteduser' : user,
        'form' : form
    }
    return render(request, 'links/profile.html', context)
