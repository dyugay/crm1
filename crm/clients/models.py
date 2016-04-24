from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
  companyOrPerson = models.CharField(max_length = 7)
  author = models.ForeignKey(User)
  addedAt = models.DateTimeField(auto_now_add = True)



class clientContactDetails(models.Model):
  clientId = models.ForeignKey(Client)
  telephoneNum1 = models.IntegerField()
  telephoneNum2 = models.IntegerField()
  telephoneNum3 = models.IntegerField()
  email1 = models.EmailField()
  email2 = models.EmailField()
  firstName = models.CharField(max_length = 20)
  lastName = models.CharField(max_length = 40)
  midleName = models.CharField(max_length = 40)
  author = models.ForeignKey(User)
  addedAt = models.DateTimeField(auto_now_add = True)


