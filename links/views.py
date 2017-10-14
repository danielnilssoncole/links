from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from links.models import Category, Page, UserProfile
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
    pages = Page.objects.filter(category=category)
    context = {'category': category,
               'pages': pages}
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

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }
    return render(request, 'links/register.html', context)

def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('links:index'))
            else:
                return HttpResponse('Your links account is disabled')
        else:
            print('invalid login details: {0}, {1}'.format(username, password))
            context = {'error': 'Invalid login details supplied.'}
            return render(request, 'links/login.html', context)
    else:
        return render(request, 'links/login.html', context)

@login_required
def restricted(request):
    return HttpResponse('Since you\'re logged in, you can see this text!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


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
