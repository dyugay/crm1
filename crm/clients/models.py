# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

class Client(models.Model):
	#manager = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING, related_name="manager")
	author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
	addedAt = models.DateField(auto_now_add = True)

	def get_url(self):
		return reverse('client',
						kwargs={'clientId':self.id})



class ClientContactDetails(models.Model):
  clientId = models.ForeignKey(Client)
  telephoneNum1 = models.CharField(max_length = 16)
  telephoneNum2 = models.CharField(max_length = 16)
  telephoneNum3 = models.CharField(max_length = 16)
  email1 = models.EmailField()
  email2 = models.EmailField()
  firstName = models.CharField(max_length = 20)
  lastName = models.CharField(max_length = 40)
  middleName = models.CharField(max_length = 40)
  author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
  addedAt = models.DateField(auto_now_add = True)


class Legal_details(models.Model):
	client = models.ForeignKey(Client)
	city = models.CharField(max_length = 20)
	address = models.CharField(max_length = 60)
	company_name = models.CharField(max_length = 40)
	author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
	changedOn = models.DateField(auto_now = True, null=True)



class LK(models.Model):
	LK = models.EmailField()
	client = models.ForeignKey(Client)
	LK_added_at = models.DateField()
	author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
	changedOn = models.DateField(auto_now = True, null = True)


class Persons(models.Model):
	client = models.ForeignKey(Client)
	firstName = models.CharField(max_length = 20)
	lastName = models.CharField(max_length = 20)
	middleName = models.CharField(max_length = 20)
	telephoneNum1 = models.CharField(max_length = 16, default='')
	telephoneNum2 = models.CharField(max_length = 16, default='')
	telephoneNum3 = models.CharField(max_length = 16, default='')
	email1 = models.EmailField(default='')
	email2 = models.EmailField(default='')
	author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
	changedOn = models.DateField(auto_now = True)

	def get_url(self):
		return reverse('changePerson',
						kwargs={'personId':self.id})
						
	def get_id_str(self):
		return str(self.id)
 


class Order(models.Model):
	status_choice = (
					('INTS', 'заинтересованность'),
					('EVAL', 'оценка'),
					('OFER', 'подготовка предложения'),
					('WAIT', 'ожидание решения клиента'),
					('DVLR', 'доставка'),
					('PROC', 'выполнение заказа'),
					('DONE', 'заказ выполнен'),
					('FAIL', 'отказ'),
				   )
	call_or_email_choice = (
						 ('call', 'звонок'),
						 ('email', 'заявка'), 
						 ('glazok', 'Glazok'),
						 ('manggis', 'Manggis'),  
						 ) 

	client = models.ForeignKey(Client)
	call_or_email = models.CharField(max_length = 8, choices=call_or_email_choice)
	status = models.CharField(max_length = 20, choices=status_choice, default='INTS')
	call_on = models.DateField(blank = True)
	contactPerson = models.ForeignKey(Persons, null=True)
	manager = models.ForeignKey(User, on_delete = models.DO_NOTHING, null=True)
	author = models.ForeignKey(User, on_delete = models.DO_NOTHING, null=True, related_name = "author")
	changedOn = models.DateField(auto_now = True, null=True)

	def get_url(self):
		return reverse('order',
						kwargs={'orderId':self.id})


	def get_first_step_description(self):
		order_process = Order_process.objects.get(order=self, step = 1) 
		return order_process.step_description
  


	def get_first_step_manager(self):
		order_process = Order_process.objects.get(order=self, step = 1)
		return order_process.manager
		
	def get_first_step_date(self):
		order_process = Order_process.objects.get(order=self, step = 1)
		return order_process.date_step
		
		
		
	#def get_focalPointFirstName(self):
		#focalPoint= Persons.objects.filter(client=self.client, focalPoint=True).values("firstName")

		#if len(focalPoint):
			#focalPointFirstName = focalPoint[0].get('firstName')
			#return focalPointFirstName
		#else:
			#return '' 
		

	#def get_focalPointTel(self):
		#focalPoint= Persons.objects.filter(client=self.client, focalPoint=True).values("telephoneNum1")

		#if len(focalPoint):
			#focalPointTel = focalPoint[0].get('telephoneNum1') 
			#return focalPointTel
		#else:
			#return '' 
		
		
	#def get_focalPointEmail(self):
		#focalPoint= Persons.objects.filter(client=self.client, focalPoint=True).values("email1")

		#if len(focalPoint):
			#focalPointEmail = focalPoint[0].get('email1') 
			#return focalPointEmail
		#else:
			#return '' 



  




class Order_process(models.Model):

  order = models.ForeignKey(Order)
  step = models.IntegerField()
  step_description = models.TextField()
  date_step = models.DateTimeField(auto_now_add = True)
  manager = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)








