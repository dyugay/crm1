# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
 # companyOrPerson = models.CharField(max_length = 7)
  author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
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
  middleName = models.CharField(max_length = 40)
  author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
  addedAt = models.DateTimeField(auto_now_add = True)

class Legal_details(models.Model):
  clientId = models.ForeignKey(Client)
  personal_ID = models.CharField(max_length=12)
  city = models.CharField(max_length = 20)
  address = models.CharField(max_length = 40)
  company_name = models.CharField(max_length = 40)
  BIN =  models.CharField(max_length = 12)
  bank_account = models.CharField(max_length = 25)
  bank = models.CharField(max_length = 20)
  author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
  addedAt = models.DateTimeField(auto_now_add = True)

class Account(models.Model):
  account = models.EmailField()
  clientId = models.ForeignKey(Client)
  account_added_at = models.DateTimeField()
  inactive = models.CharField(max_length = 1)
  author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
  addedAt = models.DateTimeField(auto_now_add = True)

#class Order_status(models.Model):
#  status = models.CharField(max_length = 20)

class Order(models.Model):
  status_choice = (
                    ('INTS', 'заинтересованность'),
                    ('EVAL', 'оценка'),
                    ('OFER', 'предложение'),
                    ('BILL', 'выставлен счет'),
                    ('PROC', 'выполнение заказа'),
                    ('DONE', 'заказ выполнен'),
                    ('FAIL', 'отказ'),
                   )
  call_or_email_choice = (
                         ('call', 'звонок'),
                         ('email', 'заявка'),   
                         ) 

  clientId = models.ForeignKey(Client)
  client_contacts = models.ForeignKey(ClientContactDetails)
  call_or_email = models.CharField(max_length = 5, choices=call_or_email_choice)
  status = models.CharField(max_length = 20, choices=status_choice)
  call_on = models.DateField(blank = True)
 # manager = models.CharField(max_length = 20)
  
 # manager = models.ForeignKey(User, on_delete = models.DO_NOTHING)


class Order_process(models.Model):

  order = models.ForeignKey(Order)
  step = models.IntegerField()
  step_description = models.TextField()
  date_step = models.DateTimeField(auto_now_add = True)
  manager = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)

class Billing(models.Model):
  account = models.ForeignKey(Account, null = True, on_delete = models.DO_NOTHING)
  month = models.CharField(max_length = 2)
  year = models.CharField(max_length = 4)
  summ = models.DecimalField(max_digits = 8, decimal_places = 2)
  author =  models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
  addedAt = models.DateTimeField(auto_now_add = True)

 



