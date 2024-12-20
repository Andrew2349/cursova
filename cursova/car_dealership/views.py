from django.http import HttpResponseRedirect
from django.shortcuts import render

import car.views
from car.models import Car, Supplier


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def forbidden(request):
    return render(request, "forbidden.html")

def not_found(request):
    return render(request, "not_found.html")

def account(request):
    return render(request, "account.html")
