# -*- coding: utf-8 -*-
from django import forms
from clients.models import Client, Order, ClientContactDetails
from clients.models import Legal_details, Persons
#, Account
from clients.models import Order, Order_process, LK
#, Billing
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import get_object_or_404 
from django.core.urlresolvers import reverse
from urllib import urlencode
from clients.helpers import check_telephoneNum, check_email


my_default_errors = {
						'required': 'Поле обязательно для заполнения',
						'invalid': 'Введенное значение некорректно'
							}


class newOrderForm(forms.Form):
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	call_or_email = forms.CharField(max_length = 8, label="Тип обращения", error_messages=my_default_errors)
	step_description = forms.CharField(label="Описание шага", error_messages=my_default_errors, initial='')
	status = forms.CharField(max_length = 20, label="Статус заказа", initial='', error_messages=my_default_errors)
	call_on = forms.DateField(label="Когда связаться с клиентом", error_messages=my_default_errors)
	manager = forms.CharField(max_length = 20, label="Менеджер заказа", error_messages=my_default_errors)
	contactPersonId = forms.IntegerField(label="Контактное лицо", error_messages=my_default_errors)
	author = forms.CharField(max_length = 20, label='Автор записи', error_messages=my_default_errors)

		
	
	#create order
	def save(self): 
		client = get_object_or_404(Client, id=self.cleaned_data.get('clientId'))
		manager = get_object_or_404(User, username=self.cleaned_data.get('manager'))
		user = get_object_or_404(User, username = self.cleaned_data.get('author')) 
		contactPerson = get_object_or_404(Persons, id=self.cleaned_data.get('contactPersonId'))
		
		order = Order(	client = client,
						status = self.cleaned_data.get('status'),
						call_on = self.cleaned_data.get('call_on'),
						call_or_email = self.cleaned_data.get('call_or_email'),
						contactPerson = contactPerson,
						manager = manager,
						author = user,
						)
		order.save()

		
		
		#create order_process
		order_process = Order_process(order = order,
										step = 1,
										step_description = self.cleaned_data.get('step_description'),
										manager = manager, 
										)      
		order_process.save()    

		return order


class orderForm(forms.Form):
	orderId = forms.CharField(max_length = 10, label='Заказ', error_messages=my_default_errors)
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	call_or_email = forms.CharField(max_length = 8, label="Тип обращения", error_messages=my_default_errors, required=False)
	step_description = forms.CharField(label="Описание шага", error_messages=my_default_errors, initial='')
	status = forms.CharField(max_length = 20, label="Статус заказа", initial='', error_messages=my_default_errors)
	call_on = forms.DateField(label="Когда связаться с клиентом", error_messages=my_default_errors)
	#focalPointId = forms.IntegerField(label='Контактное лицо', error_messages=my_default_errors)
	manager = forms.CharField(max_length = 20, label="Менеджер заказа", error_messages=my_default_errors)
	contactPersonId = forms.IntegerField(label="Контактное лицо", error_messages=my_default_errors)
	author = forms.CharField(max_length = 20, label='Автор записи')
	changedOn = forms.DateField(label='Дата изменений', error_messages=my_default_errors, required=False)
	

	
	
	
	def save(self, **kwargs):

		manager = User.objects.get(username = self.cleaned_data.get('manager')) 
		
		author = kwargs.get("author")
		author = get_object_or_404(User, username = author) 



		#save order data
		order = kwargs.get('order')
		#order.call_or_email = self.cleaned_data.get('call_or_email')
		#print order.call_or_email
		order.status = self.cleaned_data.get('status')
		order.call_on = self.cleaned_data.get('call_on')
		order.manager = manager
		order.author = author
		order.contactPerson = Persons.objects.get(id = self.cleaned_data.get('contactPersonId'))
		order.save()



		#get the last step of the order and incrementing the step
		last_step = Order_process.objects.filter(order = order).count() + 1
		
		
		#create process step
		order_process = Order_process.objects.create(order = order,
												  step = last_step,
												  step_description = self.cleaned_data.get('step_description'),
												  manager = manager,
												  )
		return order



   
class loginForm(forms.Form):
  username = forms.CharField(max_length =20, label='Логин')
  password = forms.CharField(max_length = 128, label='Пароль', widget=forms.PasswordInput)
  
  def clean(self):
    cleaned_data = super(loginForm, self).clean()
    if len(cleaned_data)!=0:
     username = cleaned_data.get('username')
     password = cleaned_data.get('password')
    
     user = authenticate(username = username, password = password)
     if user is None:
       raise forms.ValidationError("Неверные имя пользователя и/или пароль")   
    
    return cleaned_data 




class createPersonForm(forms.Form):
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	firstName = forms.CharField(max_length = 20, label='Имя', error_messages=my_default_errors, initial='')
	lastName = forms.CharField(max_length =20, label='Фамилия', error_messages=my_default_errors, required=False, initial='')
	middleName = forms.CharField(max_length = 20, label='Отчетство', error_messages=my_default_errors, required=False, initial='')
	telephoneNum1 = forms.CharField(max_length = 16, label='Телефон 1', error_messages=my_default_errors, required=False, initial='')
	telephoneNum2 = forms.CharField(max_length = 16, label='Телефон 2', error_messages=my_default_errors, required=False, initial='')
	telephoneNum3 = forms.CharField(max_length = 16, label='Телефон 3', error_messages=my_default_errors, required=False, initial='')
	email1 = forms.EmailField(max_length = 40, label='e-mail 1', error_messages=my_default_errors, required=False, initial='')
	email2 = forms.EmailField(max_length = 40, label='e-mail 2', error_messages=my_default_errors, required=False, initial='')
	#focalPoint = forms.BooleanField(label='Основной контакт', error_messages=my_default_errors, required=False, initial=False)
	author = forms.CharField(max_length = 20, label='Автор записи')


	def clean_telephoneNum1(self):
		telephoneNum1 = self.cleaned_data.get('telephoneNum1')
		if telephoneNum1:
			personId = self.cleaned_data.get('personId')
			persons = check_telephoneNum(telephoneNum1)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'Номер уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																		'firstName':person.firstName}, code='invalid')
		return telephoneNum1
	
	
	def clean_telephoneNum2(self):
		telephoneNum2 = self.cleaned_data.get('telephoneNum2')
		if telephoneNum2:
			personId = self.cleaned_data.get('personId')
			persons = check_telephoneNum(telephoneNum2)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'Номер уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return telephoneNum2
		

	def clean_telephoneNum3(self):
		telephoneNum3 = self.cleaned_data.get('telephoneNum3')
		if telephoneNum3:
			personId = self.cleaned_data.get('personId')
			persons = check_telephoneNum(telephoneNum3)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'Номер уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return telephoneNum3
	
	
	def clean_email1(self):
		email1 = self.cleaned_data.get('email1')
		if email1:
			personId = self.cleaned_data.get('personId')
			persons = check_email(email1)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'E-mail уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return email1
	
	
	def clean_email2(self):
		email2 = self.cleaned_data.get('email2')
		if email2:
			personId = self.cleaned_data.get('personId')
			persons = check_email(email2)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'E-mail уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return email2
	
	
	
	
	
	
	
		
	def save(self, **kwargs):
		client = get_object_or_404(Client, id = self.cleaned_data.get('clientId'))
		user = User.objects.get(username = self.cleaned_data.get('author'))
		person = Persons(client = client,
						 firstName = self.cleaned_data.get('firstName'),
						 lastName = self.cleaned_data.get('lastName'),
						 middleName = self.cleaned_data.get('middleName'),
						 telephoneNum1 = self.cleaned_data.get('telephoneNum1'),
						 telephoneNum2 = self.cleaned_data.get('telephoneNum2'),
						 telephoneNum3 = self.cleaned_data.get('telephoneNum3'),
						 email1 = self.cleaned_data.get('email1'),
						 email2 = self.cleaned_data.get('email2'),
						 #focalPoint = self.cleaned_data.get('focalPoint'),
						 author = user,
						 changedOn = datetime.today(),
							)
		person.save()
		return person
							

class changePersonForm(forms.Form):
	personId = forms.CharField(max_length=10, label='ID контакта', error_messages=my_default_errors)
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	firstName = forms.CharField(max_length = 20, label='Имя', error_messages=my_default_errors, initial='')
	lastName = forms.CharField(max_length =20, label='Фамилия', error_messages=my_default_errors, required=False, initial='')
	middleName = forms.CharField(max_length = 20, label='Отчетство', error_messages=my_default_errors, required=False, initial='')
	telephoneNum1 = forms.CharField(max_length = 16, label='Телефон 1', error_messages=my_default_errors, required=False, initial='')
	telephoneNum2 = forms.CharField(max_length = 16, label='Телефон 2', error_messages=my_default_errors, required=False, initial='')
	telephoneNum3 = forms.CharField(max_length = 16, label='Телефон 3', error_messages=my_default_errors, required=False, initial='')
	email1 = forms.EmailField(max_length = 40, label='e-mail 1', error_messages=my_default_errors, required=False, initial='')
	email2 = forms.EmailField(max_length = 40, label='e-mail 2', error_messages=my_default_errors, required=False, initial='')
	#focalPoint = forms.BooleanField(label='Основной контакт', error_messages=my_default_errors, required=False)
	author = forms.CharField(max_length = 20, label='Автор последнего изменения')
	changedOn = forms.DateField(label='Дата последнего изменения', required=False)



	def clean_telephoneNum1(self):
		telephoneNum1 = self.cleaned_data.get('telephoneNum1')
		if telephoneNum1:
			personId = self.cleaned_data.get('personId')
			persons = check_telephoneNum(telephoneNum1)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'Номер уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																		'firstName':person.firstName}, code='invalid')
		return telephoneNum1
	
	
	def clean_telephoneNum2(self):
		telephoneNum2 = self.cleaned_data.get('telephoneNum2')
		if telephoneNum2:
			personId = self.cleaned_data.get('personId')
			persons = check_telephoneNum(telephoneNum2)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'Номер уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return telephoneNum2
		

	def clean_telephoneNum3(self):
		telephoneNum3 = self.cleaned_data.get('telephoneNum3')
		if telephoneNum3:
			personId = self.cleaned_data.get('personId')
			persons = check_telephoneNum(telephoneNum3)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'Номер уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return telephoneNum3
		
		
	def clean_email1(self):
		email1 = self.cleaned_data.get('email1')
		if email1:
			personId = self.cleaned_data.get('personId')
			persons = check_email(email1)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'E-mail уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return email1
	
	
	def clean_email2(self):
		email2 = self.cleaned_data.get('email2')
		if email2:
			personId = self.cleaned_data.get('personId')
			persons = check_email(email2)
			if persons:
				persons = persons.exclude(id=personId)
				for person in persons:
						raise forms.ValidationError(u'E-mail уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																			'firstName':person.firstName}, code='invalid')
		return email2



		
		
		
	def save(self, **kwargs):
		person = kwargs.get('person')
		#client = kwargs.get('client')
		currentUser = User.objects.get(username = kwargs.get('currentUser'))
		
		person.firstName = self.cleaned_data.get('firstName')
		person.lastName = self.cleaned_data.get('lastName')
		person.middleName = self.cleaned_data.get('middleName')
		person.telephoneNum1 = self.cleaned_data.get('telephoneNum1')
		person.telephoneNum2 = self.cleaned_data.get('telephoneNum2')
		person.telephoneNum3 = self.cleaned_data.get('telephoneNum3')
		person.email1 = self.cleaned_data.get('email1')
		person.email2 = self.cleaned_data.get('email2')
		#person.focalPoint = self.cleaned_data.get('focalPoint')
		person.author = currentUser
		#person.changedOn = datetime.today()

		person.save()
		return person



class addLKForm(forms.Form):
	LK = forms.EmailField(max_length = 40, label='Личный кабинет', error_messages=my_default_errors, initial='')
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	LK_added_at = forms.DateField(label='Дата регистрации ЛК', error_messages=my_default_errors)
	author = forms.CharField(max_length = 20, label='Автор записи', error_messages=my_default_errors)
	changedOn = forms.DateField(label='Дата последнего изменения', required=False)
	



	def clean_LK(self):
		lk = self.cleaned_data.get('LK')
		if lk:
			LKs = LK.objects.filter(LK=lk)
			if LKs:
				for cabinet in LKs:
						raise forms.ValidationError(u'ЛК уже существует в базе, принадлежит клиенту: №%(clientId)s', params={ 'clientId': cabinet.client.id}, code='invalid')
																																		
		return lk





	def save(self, **kwargs):
		client = get_object_or_404(Client, id = self.cleaned_data.get('clientId'))
		user = get_object_or_404(User, username = self.cleaned_data.get('author')) 

		LK_inst = LK(	client=client,
						LK = self.cleaned_data.get('LK'),
						LK_added_at = self.cleaned_data.get('LK_added_at'),
						author = user
						)
						
		LK_inst.save()
		
		return LK








class changeClientLKForm(forms.Form):
	LK = forms.EmailField(max_length = 40, label='Личный кабинет', error_messages=my_default_errors, initial='')
	LK_Id = forms.CharField(max_length = 10, label='id ЛК', error_messages=my_default_errors)
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	LK_added_at = forms.DateField(label='Дата регистрации ЛК', error_messages=my_default_errors)
	author = forms.CharField(max_length = 20, label='Автор изменений', error_messages=my_default_errors)
	changedOn = forms.DateField(label='Дата последнего изменения', required=False)
	
	
	
	
	def clean(self):
		lk = self.cleaned_data.get('LK')

		if lk:
			LKs = LK.objects.filter(LK=lk)
			clientId = self.cleaned_data.get('clientId')
			#print clientId
			
			LKs = LKs.exclude(client__id = clientId)
			if LKs:
				for cabinet in LKs:
						raise forms.ValidationError(u'ЛК уже существует в базе, принадлежит клиенту: №%(clientId)s', params={ 'clientId': cabinet.client.id}, code='invalid')
																																		

	
	def save(self, **kwargs):
		lk = kwargs.get('lk')
		#client = kwargs.get('client')
		lk.LK = self.cleaned_data.get('LK')
		lk.LK_added_at = self.cleaned_data.get('LK_added_at')
		lk.author = get_object_or_404(User, username = self.cleaned_data.get('author')) 
		lk.save()
		
		return lk
	
	
class addLegalDetailsForm(forms.Form):
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	city = forms.CharField(max_length = 20, label='Город', error_messages=my_default_errors, initial='')
	address = forms.CharField(max_length = 40, label='Адрес', error_messages=my_default_errors, initial='', required=False)
	company_name = forms.CharField(max_length = 40, label='Компания', error_messages=my_default_errors, initial='', required=False)
	author = forms.CharField(max_length = 20, label='Автор изменений', error_messages=my_default_errors, required=False)
	changedOn = forms.DateField(label='Дата изменений', error_messages=my_default_errors, required=False)
	
	def save(self, **kwargs):
		client = get_object_or_404(Client, id = self.cleaned_data.get('clientId'))
		user = get_object_or_404(User, username = self.cleaned_data.get('author')) 
		
		legal_details = Legal_details(
										client = client,
										city = self.cleaned_data.get('city'),
										address = self.cleaned_data.get('address'),
										company_name = self.cleaned_data.get('company_name'),
										author = user,
											)
		legal_details.save()
		return legal_details


class changeLegalDetailsForm(forms.Form):
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors)
	city = forms.CharField(max_length = 20, label='Город', error_messages=my_default_errors, initial='')
	address = forms.CharField(max_length = 40, label='Адрес', error_messages=my_default_errors, initial='', required=False)
	company_name = forms.CharField(max_length = 40, label='Компания', error_messages=my_default_errors, initial='', required=False)
	author = forms.CharField(max_length = 20, label='Автор изменений', error_messages=my_default_errors, required=False)
	changedOn = forms.DateField(label='Дата изменений', error_messages=my_default_errors, required=False)
	
	def save(self, **kwargs):
		#client = get_object_or_404(Client, id = self.cleaned_data.get('clientId'))
		user = get_object_or_404(User, username = self.cleaned_data.get('author')) 
		legal_details = kwargs.get('legal_details')
		legal_details.city = self.cleaned_data.get('city')
		legal_details.address = self.cleaned_data.get('address')
		legal_details.company_name = self.cleaned_data.get('company_name')
		legal_details.author = user
		legal_details.save()
		return legal_details

class createClientForm(forms.Form):

	firstName = forms.CharField(max_length = 20, label='Имя', error_messages=my_default_errors, initial='')
	telephoneNum1 = forms.CharField(max_length = 16, label='Телефон', error_messages=my_default_errors, required=False, initial='')
	email1 = forms.EmailField(max_length = 40, label='E-mail', error_messages=my_default_errors, required=False, initial='')
	city = forms.CharField(max_length = 20, label = "Город", error_messages = my_default_errors, initial='', required=False)
	author = forms.CharField(max_length = 20, label='Автор записи', error_messages=my_default_errors)
	call_or_email = forms.CharField(max_length = 8, label="Тип обращения", error_messages=my_default_errors)
	step_description = forms.CharField(label="Описание шага", error_messages=my_default_errors, initial='')
	status = forms.CharField(max_length = 20, label="Статус заказа", initial='', error_messages=my_default_errors)
	call_on = forms.DateField(label="Когда связаться с клиентом", error_messages=my_default_errors)
	manager = forms.CharField(max_length = 20, label="Менеджер заказа", error_messages=my_default_errors)
	
	
	
	def clean_telephoneNum1(self):
		telephoneNum1 = self.cleaned_data.get('telephoneNum1')
		persons = check_telephoneNum(telephoneNum1)
		if persons:
			for person in persons:
				raise forms.ValidationError(u'Номер уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																	'firstName':person.firstName}, code='invalid')
		return telephoneNum1
	
	
	def clean_email1(self):
		email = self.cleaned_data.get('email1')
		if email:
			persons = check_email(email)
			if persons:
				for person in persons:
					raise forms.ValidationError(u'E-mail уже существует в базе, принадлежит клиенту: №%(clientId)s,  %(firstName)s', params={ 'clientId': person.client.id,
																																		'firstName':person.firstName}, code='invalid')
		return email

	
	
	
	
	def save(self, **kwargs):
		user = get_object_or_404(User, username = self.cleaned_data.get('author')) 
		client = Client(author=user)
		client.save()
		
		person = Persons(client=client,
						firstName=self.cleaned_data.get('firstName'),
						telephoneNum1=self.cleaned_data.get('telephoneNum1'),
						email1=self.cleaned_data.get('email1'),
						author=user,
							)
		person.save()
		
		
		manager = get_object_or_404(User, username=self.cleaned_data.get('manager'))
		
		order = Order(	client = client,
						status = self.cleaned_data.get('status'),
						call_on = self.cleaned_data.get('call_on'),
						call_or_email = self.cleaned_data.get('call_or_email'),
						manager = manager,
						contactPerson = person,
						author = user,
						)
		order.save()
		
		
		#create order_process
		order_process = Order_process(order = order,
										step = 1,
										step_description = self.cleaned_data.get('step_description'),
										manager = manager, 
										)      
		order_process.save()
		
		if self.cleaned_data.get('city'):
			legal_details = Legal_details(
									client = client,
									city = self.cleaned_data.get('city'),
									author = user,
										)
			legal_details.save()
		
		return client


class orderListFilterForm(forms.Form):
	manager = forms.CharField(max_length = 20, label="Менеджер заказа", error_messages=my_default_errors)
	status = forms.CharField(max_length = 20, label="Статус заказа", initial='', error_messages=my_default_errors)
	orderDateBegin = forms.DateField(label="Дата создания, с", error_messages=my_default_errors, required=False)
	orderDateEnd = forms.DateField(label="Дата создания, по", error_messages=my_default_errors, required=False)
	call_onBegin = forms.DateField(label="Позвонить клиенту, с", error_messages=my_default_errors, required=False)
	call_onEnd = forms.DateField(label="Позвонить клиенту, по", error_messages=my_default_errors, required=False)
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors, initial='', required=False)
	orderId = forms.CharField(max_length = 10, label='Заказ', error_messages=my_default_errors, initial='', required=False)
	firstName = forms.CharField(max_length = 20, label='Основной контакт', error_messages=my_default_errors, initial='', required=False)
	telephoneNum1 = forms.CharField(max_length = 16, label='Телефон', error_messages=my_default_errors, initial='', required=False)
	email1 = forms.CharField(max_length = 40, label='Email', error_messages=my_default_errors, initial='', required=False)
	step_description = forms.CharField(max_length = 100, label='Запрос клиента', initial='', error_messages=my_default_errors, required=False)
	call_or_email = forms.CharField(max_length = 8, label='Тип обращения', initial='', error_messages=my_default_errors, required=False)


	def get_filter_url(self, **kwars):
		pg = kwars.get('pg')
		
		firstName = self.cleaned_data.get('firstName').encode('utf-8')
		clientId = self.cleaned_data.get('clientId').encode('utf-8')
		orderId = self.cleaned_data.get('orderId').encode('utf-8')
		telephoneNum1 = self.cleaned_data.get('telephoneNum1').encode('utf-8')
		email1 = self.cleaned_data.get('email1').encode('utf-8')
		step_description = self.cleaned_data.get('step_description').encode('utf-8')
		#call_or_email = self.cleaned_data.get('call_or_email').encode('utf-8')
																						
																						
		#print call_or_email 
		#print self.cleaned_data.get('call_or_email')
		url=reverse('get_orders_list', kwargs={'pageNum': pg}) + '?'+ urlencode({'manager': self.cleaned_data.get('manager'),
																						'status': self.cleaned_data.get('status'),
																						'clientId': clientId,
																						'orderId': orderId,
																						'firstName': firstName,
																						'telephoneNum1': telephoneNum1,
																						'email1': email1,
																						'step_description': step_description,
																						'orderDateBegin': self.cleaned_data.get('orderDateBegin'),
																						'orderDateEnd': self.cleaned_data.get('orderDateEnd'),
																						'call_onBegin': self.cleaned_data.get('call_onBegin'),
																						'call_onEnd': self.cleaned_data.get('call_onEnd'),
																						'call_or_email': self.cleaned_data.get('call_or_email'),
																						})

		return url
		
		
class clientsByPersonsForm(forms.Form):
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors, initial='', required=False)
	firstName = forms.CharField(max_length = 20, label='Имя', error_messages=my_default_errors, initial='', required=False)
	lastName = forms.CharField(max_length = 20, label='Фамилия', error_messages=my_default_errors, initial='', required=False)
	telephoneNum = forms.CharField(max_length = 16, label='Телефон', error_messages=my_default_errors, initial='', required=False)
	email = forms.CharField(max_length = 40, label='Email', error_messages=my_default_errors, initial='', required=False)




	def get_filter_url(self, **kwars):
		pageNum = kwars.get('pageNum')
	
		#clientId = self.cleaned_data.get('clientId').encode('utf-8')
	
		firstName = self.cleaned_data.get('firstName').encode('utf-8')
		lastName = self.cleaned_data.get('lastName').encode('utf-8')
		telephoneNum = self.cleaned_data.get('telephoneNum').encode('utf-8')
		email = self.cleaned_data.get('email').encode('utf-8')
		
		
		
		url=reverse('get_clients_by_persons', kwargs={'pageNum': pageNum}) + '?'+ urlencode({ 
																						#'clientId': clientId,
																						'firstName': firstName,
																						'lastName': lastName,
																						'telephoneNum': telephoneNum,
																						'email': email,
																						})
	
		return url
		
	
class clientsByLegalDetailsForm(forms.Form):
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors, required=False)
	city = forms.CharField(max_length = 20, label='Город', error_messages=my_default_errors, initial='', required=False)
	address = forms.CharField(max_length = 40, label='Адрес', error_messages=my_default_errors, initial='', required=False)
	company_name = forms.CharField(max_length = 40, label='Компания', error_messages=my_default_errors, initial='', required=False)



	def get_filter_url(self, **kwars):
		pageNum = kwars.get('pageNum')

		clientId = self.cleaned_data.get('clientId').encode('utf-8')
		city = self.cleaned_data.get('city').encode('utf-8')
		address = self.cleaned_data.get('address').encode('utf-8')
		company_name = self.cleaned_data.get('company_name').encode('utf-8')

		
		
		url=reverse('get_clients_by_legal_details', kwargs={'pageNum': pageNum}) + '?'+ urlencode({ 
																						'clientId': clientId,
																						'city': city,
																						'address': address,
																						'company_name': company_name,
																						})
	
		return url
		
	


	
class clientsByLKForm(forms.Form):
	clientId = forms.CharField(max_length = 10, label='Клиент', error_messages=my_default_errors, initial='', required=False)
	LK = forms.CharField(max_length = 40, label='Личный кабинет', error_messages=my_default_errors, initial='', required=False)




	def get_filter_url(self, **kwars):
		pageNum = kwars.get('pageNum')

		LK = self.cleaned_data.get('LK').encode('utf-8')
		clientId = self.cleaned_data.get('clientId').encode('utf-8')
		
		
		url=reverse('get_clients_by_LK', kwargs={'pageNum': pageNum}) + '?'+ urlencode({ 
																						'clientId': clientId,
																						'LK': LK,
																						})
	
		return url










class report_orders_form(forms.Form):
	manager = forms.CharField(max_length = 20, label="Менеджер заказа", error_messages=my_default_errors, required=False)
	status = forms.CharField(max_length = 20, label="Статус заказа", initial='', error_messages=my_default_errors, required=False)
	orderDateBegin = forms.DateField(label="Дата создания, с", error_messages=my_default_errors, required=False)
	orderDateEnd = forms.DateField(label="Дата создания, по", error_messages=my_default_errors, required=False)
	group_by = forms.CharField(max_length = 20, label="Группировать по", initial='', error_messages=my_default_errors, required=False)
	

	def get_filter_url(self, **kwars):
		pg = kwars.get('pg')
		url=reverse('report_orders', kwargs={'pageNum': pg}) + '?'+ urlencode({
																						'manager': self.cleaned_data.get('manager'),
																						'status': self.cleaned_data.get('status'),
																						'orderDateBegin': self.cleaned_data.get('orderDateBegin'),
																						'orderDateEnd': self.cleaned_data.get('orderDateEnd'),
																						'group_by':self.cleaned_data.get('group_by'),
																						})

		return url












