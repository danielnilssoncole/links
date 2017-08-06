from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'message': 'this is the message from the index view.'}
    return render(request, 'links/index.html', context)

def about(request):
    context = {'name': 'daniel'}
    return render(request, 'links/about.html', context)
