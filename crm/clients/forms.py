# -*- coding: utf-8 -*-
from django import forms
from clients.models import Client, Order, ClientContactDetails
from clients.models import Legal_details, Account
from clients.models import Order, Order_process, Billing
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class newOrderForm(forms.Form):
  firstName = forms.CharField(max_length = 20) 
  telephoneNum1 = forms.CharField(max_length = 11)
  email1 = forms.EmailField(max_length = 100) 
  city = forms.CharField(max_length = 20)
  company_name = forms.CharField(max_length = 40)
  lastName = forms.CharField(max_length = 40)
  middleName = forms.CharField(max_length = 40)
  step_description = forms.CharField(widget = forms.Textarea)
 # date_step = forms.DateTimeField()
  call_on = forms.DateField(widget = forms.SelectDateWidget(empty_label="Nothing"))
  manager = forms.CharField(max_length = 20)
  




# create order
  def save(self):
     #create client
     manager = User.objects.get(username=self.cleaned_data.get('manager'))
     client = Client(author = manager)
     client.save()
    
     #create client contact details
     clientContactDetails = ClientContactDetails(clientId = client, 
                                                 firstName = self.cleaned_data.get('firstName'),
                                                 telephoneNum1 = self.cleaned_data.get('telephoneNum1'),
                                                 email1 = self.cleaned_data.get('email1'),
                                                 lastName = self.cleaned_data.get('lastName'),
                                                 middleName = self.cleaned_data.get('middleName'),
                                                 author = manager     
                                                  )
     clientContactDetails.save()
    
     #create client legal details
     legalDetails = Legal_details(clientId = client,
                                  city = self.cleaned_data.get('city'),
                                  company_name = self.cleaned_data.get('company_name'),
                                  author = manager
                                  )
     legalDetails.save()  
   
   
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



 

    



   

