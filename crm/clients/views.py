# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from clients.forms import newOrderForm, loginForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse



# main page
def main(request, *args, **kwargs):
 if request.user.is_authenticated():
   return render(request,
                 'main.html',
                 ) 
 else:
  return HttpResponse('you are not authorized')





# new order creation 
@login_required
def createOrder(request, *args, **kwargs):
 if request.method == 'POST':
  form = newOrderForm(request.POST)
  if form.is_valid():
   order = form.save()
   url = reverse('order')
   return HttpResponseRedirect(url)
 else:   
   initial_data = {'manager': request.user}
   form = newOrderForm(initial = initial_data)
 
 return render(request, 
                 'createOrder.html',
                 {
                  'form': form, 
                 }
                ) 



#order 
def order(request, *args, **kwargs):
  return HttpResponse('It is an order form!')


#login
def loginUser(request, *args, **kwargs):
  if request.method == 'POST':
    form = loginForm(request.POST)
    if form.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username, password=password)
      if user.is_active:
       login(request, user)
       url = request.GET.get('next')
       if url is None:
        url = reverse('main')
       return HttpResponseRedirect(url)
      else:
       return HttpResponse('user is not active') 
  else:
    form = loginForm()
 
  return render(request, 
                  'LoginForm.html',
                  {
                    'form': form,     
                   }  )


#logout
def logoutUser(request, *args, **kwargs):
  logout(request)
  url = reverse('main')
  return HttpResponseRedirect(url)







