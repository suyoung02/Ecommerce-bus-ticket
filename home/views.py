from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *
def home(request):
    return render(request,'home/homepage.html')