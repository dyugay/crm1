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
  #focalPoint = models.CharField(max_length = 1, null = True)
  author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
  addedAt = models.DateField(auto_now_add = True)


class Legal_details(models.Model):
	client = models.ForeignKey(Client)
	city = models.CharField(max_length = 20)
	address = models.CharField(max_length = 40)
	company_name = models.CharField(max_length = 40)
	author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
	changedOn = models.DateField(auto_now = True, null=True)

  #BIN =  models.CharField(max_length = 12)
  #bank_account = models.CharField(max_length = 25)
  #bank = models.CharField(max_length = 20)
  #personal_ID = models.CharField(max_length=12)


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
	#focalPoint = models.BooleanField(default=False)
	author = models.ForeignKey(User, null = True, on_delete = models.DO_NOTHING)
	changedOn = models.DateField(auto_now = True)

	def get_url(self):
		return reverse('changePerson',
						kwargs={'personId':self.id})
						
	def get_id_str(self):
		return str(self.id)
 
#class Order_status(models.Model):
#  status = models.CharField(max_length = 20)

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
						 ) 

	client = models.ForeignKey(Client)
	call_or_email = models.CharField(max_length = 5, choices=call_or_email_choice)
	status = models.CharField(max_length = 20, choices=status_choice, default='INTS')
	call_on = models.DateField(blank = True)
	contactPerson = models.ForeignKey(Persons, null=True)
	manager = models.ForeignKey(User, on_delete = models.DO_NOTHING, null=True)

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

#class Billing(models.Model):
  #account = models.ForeignKey(Account, null = True, on_delete = models.DO_NOTHING)
  #month = models.CharField(max_length = 2)
  #year = models.CharField(max_length = 4)
  #summ = models.DecimalField(max_digits = 8, decimal_places = 2)
  #author =  models.F	oreignKey(User, null = True, on_delete = models.DO_NOTHING)
  #addedAt = models.DateTimeField(auto_now_add = True)

 


#def get_order_related_data(order):
# create order data  
#  order_related_data = {'orderId': order.id,
#                        'clientId':order.clientId.id, 
#                        'call_or_email': order.call_or_email,
#                        'status': order.status,
#                        'call_on': order.call_on,
#                        }

# create client contact details
#  client_contact_details = ClientDontactDetails.objects.get(ClientContactDetails=) 
  

# create order_process data
#  order_process = Order_process.objects.filter(order=order)  
   
  
#  return order_related_data






