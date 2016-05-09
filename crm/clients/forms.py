# -*- coding: utf-8 -*-
from django import forms
from clients.models import Client, Order, ClientContactDetails
from clients.models import Legal_details, Account, Order_status
from clients.models import Order, Order_process, Billing
from django.contrib.auth import authenticate

class newOrderForm(forms.Form):
  firstName = forms.CharField(max_length = 20) 
  telephoneNum1 = forms.CharField(max_length = 11)
  email1 = forms.EmailField(max_length = 100) 
  city = forms.CharField(max_length = 20)
  company_name = forms.CharField(max_length = 40)
  lastName = forms.CharField(max_length = 40)
  middleName = forms.CharField(max_length = 40)
  step_description = forms.CharField(widget = forms.Textarea)
  date_step = forms.DateTimeField()
  manager = forms.CharField(max_length = 20)





# save order
  #def save(self):
 #  order = 

   
  # return order


class loginForm(forms.Form):
  username = forms.CharField(max_length =20)
  password = forms.CharField(max_length = 128, widget=forms.PasswordInput)
  
  def clean(self):
    cleaned_data = super(loginForm, self).clean()
    if len(cleaned_data)!=0:
     username = cleaned_data.get('username')
     password = cleaned_data.get('password')
    
     user = authenticate(username = username, password = password)
     if user is None:
       raise forms.ValidationError("Неверные имя пользователя и/или пароль")   
    
    return cleaned_data 


#  def clean_username(self):
 #   username = self.cleaned_data['username']
   
  #  if is_empty(username):
   #   raise forms.ValidationError("Введите имя пользователя")
   
   # return username     



#def is_empty(text):
#  return(text.isspace())



 

    



   

