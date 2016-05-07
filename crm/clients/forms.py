from django import forms

class newOrderForm(forms.Form):
  firstName = forms.CharField(max_length = 20) 
  telephoneNum1 = forms.CharField(max_length = 11)
  email1 = forms.EmailField(max_length = 100) 

