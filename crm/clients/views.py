# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from clients.forms import newOrderForm, loginForm, orderForm #, clientForm
from clients.forms import createPersonForm, changePersonForm, addLKForm, changeClientLKForm
from clients.forms import addLegalDetailsForm, changeLegalDetailsForm, createClientForm
from clients.forms import orderListFilterForm, clientsByPersonsForm, clientsByLKForm
from clients.forms import clientsByLegalDetailsForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from clients.models import Order, Order_process, Client, Persons, LK, Legal_details
from clients.helpers import get_order_related_data, paginate, initOrderFilterFormData, initClientsByLKFormData
from clients.helpers import initClientsByPersonsFormData
from clients.helpers import get_client_data, get_that_clientId_url, get_orders, get_clients_by_persons_search_criteria
from clients.helpers import get_clients_by_LK_search_criteria, get_clients_by_legal_details_search_criteria, initClientsByLegalDetailsFormData
from clients.helpers import get_status_numbers
from django.contrib.auth.models import User
from django.contrib import messages

# main page
@login_required
def main(request, *args, **kwargs):
	status_numbers = get_status_numbers()
	conversion_rate = round(float(status_numbers.get('DONE'))/float(status_numbers.get('total_number')), 3) * 100
	conversion_rate = str(conversion_rate) + "%"
	return render(request,
					'main.html',
					{
					'ints_number': status_numbers.get('INTS'),
					'eval_number': status_numbers.get('EVAL'),
					'ofer_number': status_numbers.get('OFER'),
					'wait_number': status_numbers.get('WAIT'),
					'dvlr_number': status_numbers.get('DVLR'),
					'proc_number': status_numbers.get('PROC'),
					'done_number': status_numbers.get('DONE'),
					'fail_number': status_numbers.get('FAIL'),
					'total_number': status_numbers.get('total_number'),
					'conversion_rate': conversion_rate,
					}
						) 






# new order creation 
@login_required
def createOrder(request, *args, **kwargs):
	initial_data = {'clientId': kwargs.get('clientId')}

	users = User.objects.all()
	persons = Persons.objects.filter(client=kwargs.get('clientId'))
	
	if request.method == 'POST':
		form = newOrderForm(request.POST)
		if form.is_valid():
			order = form.save()
			url = order.client.get_url()
			return HttpResponseRedirect(url)
	else:
		initial_data['manager'] = request.user.username
		form = newOrderForm(initial = initial_data)

	return render(request, 
					'order.html',
					{
					'form': form,
					'users': users,
					'persons': persons,
							}
								) 



#order 
@login_required
def order(request, *args, **kwargs):
	
	#capturing parameters by url 
	orderId = kwargs['orderId']
	order = get_object_or_404(Order, id = orderId)
	users = User.objects.all()
	persons = Persons.objects.filter(client=order.client)
	order_process = Order_process.objects.filter(order=order).order_by('-step')

	#initialization form
	initial_data = get_order_related_data(order)

 
	if request.method == 'POST':
		form = orderForm(request.POST)
		if form.is_valid():
			order =  form.save(order = order)
			url = order.get_url()
			messages.success(request, 'Шаг создан')
			return HttpResponseRedirect(url)
	  
	else:

		##manager field initialization
		#initial_data['manager'] = request.user.username
		form = orderForm(initial = initial_data)


	return render(request,
	                'order.html',
	                {
	                 'form': form,
	                 'order': order,
	                 'order_process': order_process,
	                 'users': users,
	                 'persons': persons,
	                } 
	                  )







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




# orders list
@login_required
def get_orders_list(request, *args, **kwargs):


	
	if request.method=='POST':
		form=orderListFilterForm(request.POST)
		if form.is_valid():
			url = form.get_filter_url(pg=kwargs.get('pageNum'))
			return HttpResponseRedirect(url)
		else:
			return render(
				request,
				'orders_list.html',
				{
					'form': form,
				}
				)
	else:
		orders_list = get_orders(request)
		status_numbers = get_status_numbers(request=request)
		paginatorAttr = paginate(request, orders_list, kwargs.get('pageNum'))
		users = User.objects.all()
		initial_data = initOrderFilterFormData(request)
		form=orderListFilterForm(initial=initial_data)

	
		return render(
					   request,
					   'orders_list.html',
					   {'paginator': paginatorAttr.get('paginator'),
						'page': paginatorAttr.get('page'),
						'right_offset': paginatorAttr.get('right_offset'),
						'left_offset': paginatorAttr.get('left_offset'),
						'display_range': paginatorAttr.get('display_range'),
						'form': form,
						'users': users,
						'ints_number': status_numbers.get('INTS'),
						'eval_number': status_numbers.get('EVAL'),
						'ofer_number': status_numbers.get('OFER'),
						'wait_number': status_numbers.get('WAIT'),
						'dvlr_number': status_numbers.get('DVLR'),
						'proc_number': status_numbers.get('PROC'),
						'done_number': status_numbers.get('DONE'),
						'fail_number': status_numbers.get('FAIL'),
						}
						 )





#client
@login_required
def client(request, *args, **kwargs):
	clientId = kwargs['clientId']
	client = get_object_or_404(Client, id = clientId)

	persons = Persons.objects.filter(client=client)
	lks = LK.objects.filter(client = client)
	legal_details = Legal_details.objects.filter(client=client)
	orders_list = Order.objects.filter(client=client).order_by('-id')
	users = User.objects.all()
	
	return render(
	               request,
	               'client.html',
	               {
	                'client':client,
	                'persons':persons,
	                #'form':form,
	                'users': users,
	                'lks': lks,
	                'legal_details': legal_details,
	                'orders_list': orders_list,
	                }
	                 )

# create client
@login_required
def createClient(request, *args, **kwargs):
	users = User.objects.all()
	initial_data={}
	if request.method=='POST':
		form = createClientForm(request.POST)
		if form.is_valid():
			client = form.save()
			url = client.get_url()
			return HttpResponseRedirect(url)
			
	else:
		initial_data.update({'author':request.user.username, 
							 'manager': request.user.username})
		#initial_data['manager'] = request.user.username
		form = createClientForm(initial=initial_data)

	return render(
	               request,
	               'createClient.html',
	               {
	                'form':form,
	                'users': users,
	                }
	                 )




#create person
@login_required
def createPerson(request, *args, **kwargs):
	clientId = kwargs.get('clientId')
	initial_data = {'clientId':clientId}

	if request.method=='POST':
		form = createPersonForm(request.POST)
		if form.is_valid():
			person = form.save()
			url = get_that_clientId_url(clientId)
			return HttpResponseRedirect(url)
			
	else:
		initial_data.update({'author':request.user})
		form = createPersonForm(initial=initial_data)
	return render(
					request,
					'Person.html',
					{
						'form':form,
							}
						)
						
						
#change person
@login_required
def changePerson(request, *args, **kwargs):
	#clientId = kwargs.get('clientId')
	personId = kwargs.get('personId')
	person = Persons.objects.get(id = personId)
	client = Client.objects.get(id=person.client.id)

	initial_data = {
					'clientId': client.id, 
					'personId': person.id,
					'firstName': person.firstName,
					'lastName': person.lastName,
					'middleName': person.middleName,
					'telephoneNum1': person.telephoneNum1,
					'telephoneNum2': person.telephoneNum2,
					'telephoneNum3': person.telephoneNum3,
					'email1': person.email1,
					'email2': person.email2,
					#'focalPoint': person.focalPoint,
					'author': person.author,
					'changedOn': person.changedOn,
					}
					
	if request.method == 'POST':
		form = changePersonForm(request.POST)
		if form.is_valid():
			person = form.save( #client=client,
								currentUser=request.user,
								person=person)
			url = person.get_url()
			messages.success(request, 'Контакты сохранены')
			return HttpResponseRedirect(url)
	else:
		
		form = changePersonForm(initial=initial_data)
	
	return render( 
					request,
					'Person.html',
					{
						'form': form,
					})
#add LK
@login_required
def addLK(request, *args, **kwargs):
	initial_data = {'clientId': kwargs.get('clientId'),
					'author': request.user}
	if request.method=='POST':
		form = addLKForm(request.POST)
		if form.is_valid():
			LK = form.save()
			client = get_object_or_404(Client, id = initial_data.get('clientId'))
			url = client.get_url()
			return HttpResponseRedirect(url)
	else:
		form = addLKForm(initial=initial_data)
	
	return render(
					request,
					'LK.html',
					{
						'form':form,
						}
					)


#change LK in connection with client
@login_required
def changeClientLK(request, *args, **kwargs):
	lk = get_object_or_404(LK, id = kwargs.get('LK_Id'))
	client = get_object_or_404(Client, id = lk.client.id)
	
	initial_data = {
					'clientId': client.id,
					'LK_Id': lk.id,
					'LK': lk.LK,
					'LK_added_at': lk.LK_added_at,
					'author': request.user,
					'changedOn': lk.changedOn
					}
					
	if request.method=='POST':
		form = changeClientLKForm(request.POST)
		if form.is_valid():
			lk = form.save(
							#client=client,
							lk = lk,
							)
			url = client.get_url()
			return HttpResponseRedirect(url)
	else:
		form = changeClientLKForm(initial=initial_data)
	
	return render(
					request,
					'LK.html',
					{
						'form':form,
						}
					)

#add legal details - company name, address, city
@login_required
def addLegalDetails(request, *args, **kwargs):
	initial_data = {'clientId': kwargs.get('clientId'),
					'author': request.user}
	if request.method=='POST':
		form = addLegalDetailsForm(request.POST)
		if form.is_valid():
			legal_details = form.save()
			client = get_object_or_404(Client, id = initial_data.get('clientId'))
			url = client.get_url()
			return HttpResponseRedirect(url)
	else:
		form = addLegalDetailsForm(initial=initial_data)
	
	return render(
					request,
					'legalDetails.html',
					{
						'form':form,
						}
					)

#change legal details - company name, address, city
@login_required
def changeLegalDetails(request, *args, **kwargs):

	legal_details = get_object_or_404(Legal_details, id=kwargs.get('legal_details_id'))
	
	initial_data = {'legal_details_id': kwargs.get('legal_details_id'),
					'clientId': legal_details.client.id,
					'city': legal_details.city,
					'address': legal_details.address,
					'company_name': legal_details.company_name,
					'changedOn': legal_details.changedOn,
					'author': request.user,
						}
	if request.method=='POST':
		form = changeLegalDetailsForm(request.POST)
		if form.is_valid():
			legal_details = form.save(legal_details=legal_details)
			client = get_object_or_404(Client, id = initial_data.get('clientId'))
			url = client.get_url()
			return HttpResponseRedirect(url)
	else:
		form = changeLegalDetailsForm(initial=initial_data)
	
	return render(
					request,
					'legalDetails.html',
					{
						'form':form,
						}
					)
					
					
					
					
					

#get clients according to persons search criterias
@login_required
def get_clients_by_persons(request, *args, **kwargs):


	if request.method=='POST':

		form=clientsByPersonsForm(request.POST)
		if form.is_valid():
			url = form.get_filter_url(pageNum=kwargs.get('pageNum'))
			return HttpResponseRedirect(url)
			
		else:
			return render(
						   request,
						   'clients_list_by_persons.html',
						   {
						   'form': form,
							}
							 )
			
		
	else:
		persons = get_clients_by_persons_search_criteria(request)
		paginatorAttr = paginate(request, persons, kwargs.get('pageNum'))
		users = User.objects.all()
		initial_data = initClientsByPersonsFormData(request)
		form=clientsByPersonsForm(initial = initial_data)
		return render(
					   request,
					   'clients_list_by_persons.html',
					   {'paginator': paginatorAttr.get('paginator'),
					   'page': paginatorAttr.get('page'),
					   'right_offset': paginatorAttr.get('right_offset'),
					   'left_offset': paginatorAttr.get('left_offset'),
					   'display_range': paginatorAttr.get('display_range'),
					   'form': form,
					   'users': users,
						}
						 )
	
#get clients according to LK search criterias
@login_required
def get_clients_by_LK(request, *args, **kwargs):


	if request.method=='POST':

		form=clientsByLKForm(request.POST)
		if form.is_valid():
			url = form.get_filter_url(pageNum=kwargs.get('pageNum'))
			return HttpResponseRedirect(url)
			
		else:
			return render(
						   request,
						   'clients_list_by_LK.html',
						   {
						   'form': form,
							}
							 )
			
		
	else:
		LKs = get_clients_by_LK_search_criteria(request)
		paginatorAttr = paginate(request, LKs, kwargs.get('pageNum'))
		users = User.objects.all()
		initial_data = initClientsByLKFormData(request)
		form=clientsByLKForm(initial = initial_data)
		return render(
					   request,
					   'clients_list_by_LK.html',
					   {'paginator': paginatorAttr.get('paginator'),
					   'page': paginatorAttr.get('page'),
					   'right_offset': paginatorAttr.get('right_offset'),
					   'left_offset': paginatorAttr.get('left_offset'),
					   'display_range': paginatorAttr.get('display_range'),
					   'form': form,
					   'users': users,
						}
						 )


	
#get clients according to legal details search criterias
@login_required
def get_clients_by_legal_details(request, *args, **kwargs):


	if request.method=='POST':

		form=clientsByLegalDetailsForm(request.POST)
		if form.is_valid():
			url = form.get_filter_url(pageNum=kwargs.get('pageNum'))
			return HttpResponseRedirect(url)
			
		else:
			return render(
						   request,
						   'clients_list_by_legal_details.html',
						   {
						   'form': form,
							}
							 )
			
		
	else:
		legal_details = get_clients_by_legal_details_search_criteria(request)
		paginatorAttr = paginate(request, legal_details, kwargs.get('pageNum'))
		users = User.objects.all()
		initial_data = initClientsByLegalDetailsFormData(request)
		form=clientsByLegalDetailsForm(initial = initial_data)
		return render(
					   request,
					   'clients_list_by_legal_details.html',
					   {'paginator': paginatorAttr.get('paginator'),
					   'page': paginatorAttr.get('page'),
					   'right_offset': paginatorAttr.get('right_offset'),
					   'left_offset': paginatorAttr.get('left_offset'),
					   'display_range': paginatorAttr.get('display_range'),
					   'form': form,
					   'users': users,
						}
						 )
