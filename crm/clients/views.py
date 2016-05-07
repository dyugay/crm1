from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def test(request, *args, **kwargs):
 return HttpResponse('Test is OK!')
 
# new order creation 
def createOrder(request, *args, **kwargs):
 return HttpResponse('It is a new order!')


