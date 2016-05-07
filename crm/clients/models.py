from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
  companyOrPerson = models.CharField(max_length = 7)
  author = models.ForeignKey(User)
  addedAt = models.DateTimeField(auto_now_add = True)



class ClientContactDetails(models.Model):
  clientId = models.ForeignKey(Client)
  telephoneNum1 = models.CharField(max_length = 11)
  telephoneNum2 = models.CharField(max_length = 11)
  telephoneNum3 = models.CharField(max_length = 11)
  email1 = models.EmailField()
  email2 = models.EmailField()
  firstName = models.CharField(max_length = 20)
  lastName = models.CharField(max_length = 40)
  midleName = models.CharField(max_length = 40)
  author = models.ForeignKey(User)
  addedAt = models.DateTimeField(auto_now_add = True)

class Legal_details(models.Model):
  cleintId = models.ForeignKey(Client)
  personal_ID = models.CharField(max_length=12)
  city = models.CharField(max_length = 20)
  company_name = models.CharField(max_length = 40)
  BIN =  models.CharField(max_length = 12)
  bank_account = models.CharField(max_length = 25)
  bank = models.CharField(max_length = 20)
  author = models.ForeignKey(User)
  addedAt = models.DateTimeField(auto_now_add = True)

class Account(models.Model):
  account = models.EmailField()
  clientId = models.ForeignKey(Client)
  account_added_at = models.DateTimeField()
  inactive = models.CharField(max_length = 1)
  author = models.ForeignKey(User)
  addedAt = models.DateTimeField(auto_now_add = True)

class Order_status(models.Model):
  status = models.CharField(max_length = 20)

class Order(models.Model):
  clientID = models.ForeignKey(Client)
  client_contacts = models.ForeignKey(ClientContactDetails)
  tel_or_email = models.CharField(max_length = 5)
  status = models.ForeignKey(Order_status)
  manager = models.ForeignKey(User)
  


class Order_process(models.Model):
  order = models.ForeignKey(Order)
  step = models.IntegerField()
  step_description = models.TextField()
  date_step = models.DateTimeField()
  

class Billing(models.Model):
  account = models.ForeignKey(Account)
  month = models.CharField(max_length = 2)
  year = models.CharField(max_length = 4)
  summ = models.DecimalField(max_digits = 8, decimal_places = 2)
  author =  models.ForeignKey(User)
  addedAt = models.DateTimeField(auto_now_add = True)

 



