from django.shortcuts import render
from django.http import HttpResponse
from clients.forms import newOrderForm

# Create your views here.
def test(request, *args, **kwargs):
 return HttpResponse('Test is OK!')
 

# new order creation 
def createOrder(request, *args, **kwargs):
 form = newOrderForm
# return HttpResponse('It is a new order!')
 return render(request, 
                'createOrder.html',
                {
                 'form': form, 
                }
               ) 

