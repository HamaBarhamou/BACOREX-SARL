from django.shortcuts import render
from django.http import HttpResponse

def home_dao(request):
    return HttpResponse("welcom at home in dao")
