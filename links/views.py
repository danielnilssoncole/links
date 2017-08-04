from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('links - test response')

def about(request):
    return HttpResponse('links - about page')
