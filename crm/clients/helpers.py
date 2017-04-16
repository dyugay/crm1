# -*- coding: utf-8 -*-
from clients.models import ClientContactDetails, Legal_details, Client
from clients.models import Order_process, Order, Persons, LK
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta, date
from django.db.models import Q
from calendar import monthrange


#get data that is related to the order
def get_order_related_data(order):
	if order.contactPerson:
		contactPersonId = str(order.contactPerson.id)
	else:
		contactPersonId = ''

	# get order data  
	order_related_data = {'orderId': order.id,
						'clientId':order.client.id,
						'call_or_email': order.call_or_email,
						'status': order.status,
						'call_on': order.call_on,
						'contactPersonId': contactPersonId, #str(order.contactPerson.id),
						'manager': order.manager.username,
						'changedOn': order.changedOn,
						'author': order.author,
						}

	
	return order_related_data



#paginate the list from querySet
def paginate(request, querySet, page):

#   gets and checks get-paratmeter 'limit'
#   limit is a number of elements per page. default is 10
 try: 
		limit = int(request.GET.get('limit', 10))
 except ValueError:
		limit = 10
 if limit > 100:
		limit = 10
		
		
#   gets and checks get-parameter 'page'
#   page is a number of page that should be shown on the web page. default is 1
 try:
	#page = int(request.GET.get('pageNum', 3))
	#debug
	if not page:
		page = 1
	else:	
		page = int(page)
#	print page	
	#print request.GET.get('page')		
 
 except ValueError:
    raise Http404
		



 paginator = Paginator(querySet, limit)
  
    
#   gets and checks page object (page mustn't be empty)
#   if page is empty it will be the last page    
 try:
    page = paginator.page(page)
 except EmptyPage: 
	page = paginator.page(paginator.num_pages)
		
		
#set range of pages 
 left_offset = page.number - 5
 if left_offset <= 0:
	 left_offset = 1
	 
 right_offset = left_offset + 11 
 
 if right_offset >= paginator.num_pages:
	 right_offset = paginator.num_pages + 1
	 left_offset = right_offset - 11
	 if left_offset <= 0:
		 left_offset = 1
  
 display_range = []
 for pg in range(left_offset, right_offset):
	  display_range.append(pg)	 
 
 
 
##debug 
 #print left_offset
 #print right_offset 		
		
#   create paginator attributes
 paginatorAttr = { 'page': page,
                      'limit': limit,
                      'paginator': paginator,
                      'left_offset': left_offset,
                      'right_offset': right_offset, 
                      'display_range': display_range,
                         }
                         
                         
 return paginatorAttr		
    		



def get_client_data(client):
	

#   check the none value in order to avoid showing 'NONE' value in a form	
	#if not client.LK:
	 #LK=''
	#else:
	 #LK = client.LK	 
	client_data = {
	                'clientId': client.id,
	                #'LK': LK,
	                #'account_added_at': client.account_added_at,
	                'author': client.author,
	                'addedAt': client.addedAt,
	                 }
	                 
	                 
	## get client contact details
	#try:
		#client_contact_details = ClientContactDetails.objects.get(clientId=client)
	#except ClientContactDetails.DoesNotExist:
		#client_contact_details = None                 


	#client_data.update({
						#'client_contact_details': client_contact_details
							#})

	#get legal details
	try:
		legal_details = Legal_details.objects.get(client = client)
		client_data.update({'city': legal_details.city,
                            'company_name': legal_details.company_name,
                            'client_legal_details': legal_details,
                              })

	except Legal_details.DoesNotExist:
		legal_details = None

	return client_data
	
	
	
def get_that_clientId_url(id):
	return reverse('client',
					kwargs={'clientId':id})

	















"""that function is intended for getting orders qs according to search parameters given as *kwargs """
"""it's like creating queryset:
	#orders = Order_process.objects.filter(order__id__iregex = search_orderId_str, 
									#order__client__id__iregex = search_clientId_str,
									#order__contactPerson__firstName__iregex = search_firstName_str,
									#order__contactPerson__telephoneNum1__iregex = search_telephoneNum1_str,
									#order__contactPerson__email1__iregex = search_email1_str,
									#order__status__iregex = search_status_str,
									#order__manager__username__iregex = search_manager_str,
									#step_description__iregex = search_step_description_str,
									#step = 1,
									#).order_by('-id')"""
def get_orders(request):

	orders = Order_process.objects.filter(step=1)


	#search string for client id
	if request.GET.get('clientId'):
		search_clientId_str = request.GET.get('clientId')
		search_clientId_str = replace_special_symbols_str(search_clientId_str)
		orders = orders.filter(order__client__id__iregex = search_clientId_str) 



	#searxch string for orderId
	if request.GET.get('orderId'):
		search_orderId_str = request.GET.get('orderId')
		search_orderId_str = replace_special_symbols_str(search_orderId_str)
		orders = orders.filter(order__id__iregex = search_orderId_str) 




	#search string for firstName
	if request.GET.get('firstName'):
		search_firstName_str = request.GET.get('firstName')
		search_firstName_str = replace_special_symbols_str(search_firstName_str)
		orders = orders.filter(order__contactPerson__firstName__iregex = search_firstName_str)

		
	#search string for telephoneNum1
	if request.GET.get('telephoneNum1'):
		search_telephoneNum1_str = request.GET.get('telephoneNum1')
		search_telephoneNum1_str = replace_special_symbols_str(search_telephoneNum1_str)
		orders = orders.filter(order__contactPerson__telephoneNum1__iregex = search_telephoneNum1_str)


	#search string for email1
	if request.GET.get('email1'):
		search_email1_str = request.GET.get('email1')
		search_email1_str = replace_special_symbols_str(search_email1_str)
		orders = orders.filter(order__contactPerson__email1__iregex = search_email1_str)





	#search string for step_description
	if request.GET.get('step_description'):
		search_step_description_str = request.GET.get('step_description')
		search_step_description_str = replace_special_symbols_str(search_step_description_str)
		orders = orders.filter(step_description__iregex = search_step_description_str)
		
	
	#search string for call_or_email
	if request.GET.get('call_or_email') != "all" and request.GET.get('call_or_email') != None:
			orders = orders.filter(order__call_or_email = request.GET.get('call_or_email'))


	#search string for status
	if request.GET.get('status') != "all" and request.GET.get('status') != None:
			orders = orders.filter(order__status = request.GET.get('status'))
			
	
	

	#search string for manager
	if request.GET.get('manager') != "all" and request.GET.get('manager') != None:
			orders = orders.filter(order__manager__username = request.GET.get('manager'))
			


	#search for orderDate
	if request.GET.get('orderDateBegin') \
		and request.GET.get('orderDateEnd') \
		and request.GET.get('orderDateBegin') != 'None' \
		and request.GET.get('orderDateEnd') != 'None':
		
			#make some transformation beacause last date is condering by django as date and 00:00:00 time
			orderDateEnd = datetime.strptime(request.GET.get('orderDateEnd'), "%Y-%m-%d") + timedelta(days=1)
		
			orders = orders.filter(date_step__range=(request.GET.get('orderDateBegin'), orderDateEnd))


	#search for call_on
	if request.GET.get('call_onBegin') \
		and request.GET.get('call_onEnd') \
		and request.GET.get('call_onBegin') != 'None' \
		and request.GET.get('call_onEnd') != 'None':
		
			
			call_onEnd = datetime.strptime(request.GET.get('call_onEnd'), "%Y-%m-%d")
		
			orders = orders.filter(order__call_on__range=(request.GET.get('call_onBegin'), call_onEnd))

	orders = orders.order_by('-id')


	return orders
	













 
 
def initOrderFilterFormData(request):

	if not request.GET.get('clientId'):
		clientId = ''
	else:
		clientId = request.GET.get('clientId')
	
	
	if not request.GET.get('orderId'):
		orderId = ''
	else:
		orderId = request.GET.get('orderId')
	
	
	if not request.GET.get('firstName'):
		firstName = ''
	else:
		firstName = request.GET.get('firstName')
	
	
	if not request.GET.get('telephoneNum1'):
		telephoneNum1 = ''
	else:
		telephoneNum1 = request.GET.get('telephoneNum1')
	
	if not request.GET.get('email1'):
		email1 = ''
	else:
		email1 = request.GET.get('email1')
	
	if not request.GET.get('step_description'):
		step_description = ''
	else:
		step_description = request.GET.get('step_description')




	if request.GET.get('orderDateBegin') == None:
		orderDateBegin = str(date(2011, 01, 01))
	else:
		orderDateBegin = request.GET.get('orderDateBegin')
	

	if request.GET.get('orderDateEnd') == None:
		orderDateEnd = str(date.today())
	else:
		orderDateEnd = request.GET.get('orderDateEnd')
	

	if request.GET.get('call_or_email') == None:
		call_or_email = 'all'
	else:
		call_or_email = request.GET.get('call_or_email')
		
		

	if request.GET.get('status') == None:
		status = 'all'
	else:
		status = request.GET.get('status')
		
		
					
	if request.GET.get('manager') == None:
		manager = 'all'
	else:
		manager = request.GET.get('manager')
					
					
					
	if request.GET.get('call_onBegin') == None:
		call_onBegin = str(date(2011, 01, 01))
	else:
		call_onBegin = request.GET.get('call_onBegin')
	

	#if request.GET.get('call_onEnd') == None:
		#call_onEnd = str(date.today())
	#else:
		#call_onEnd = request.GET.get('call_onEnd')
					
					
					
	initial_data = {'manager': manager, 
					'status': status, 
					'orderDateBegin': orderDateBegin, 
					'orderDateEnd': orderDateEnd, 
					'call_onBegin': call_onBegin, 
					'call_onEnd': request.GET.get('call_onEnd'), #call_onEnd,
					'clientId': clientId,
					'orderId': orderId,
					'firstName': firstName,
					'telephoneNum1': telephoneNum1,
					'email1': email1,
					'step_description': step_description,
					'call_or_email': call_or_email,
					}
	
	return initial_data
 
 
 
 
 
def initClientsByPersonsFormData(request):

	
	
	if not request.GET.get('firstName'):
		firstName = ''
	else:
		firstName = request.GET.get('firstName')
	
	
	if not request.GET.get('lastName'):
		lastName = ''
	else:
		lastName = request.GET.get('lastName')
	
	
	if not request.GET.get('telephoneNum'):
		telephoneNum = ''
	else:
		telephoneNum = request.GET.get('telephoneNum')
	
	
	if not request.GET.get('email'):
		email = ''
	else:
		email = request.GET.get('email')
	
			
				
				
					
	initial_data = {
					'firstName': firstName,
					'lastName': lastName,
					'telephoneNum': telephoneNum,
					'email': email,
					}
	
	return initial_data
 
 
def initClientsByLKFormData(request):

	if not request.GET.get('clientId'):
		clientId = ''
	else:
		clientId = request.GET.get('clientId')

	
	if not request.GET.get('LK'):
		LK = ''
	else:
		LK = request.GET.get('LK')
	
	

	initial_data = {
					'clientId': clientId,
					'LK': LK,
					}
	
	return initial_data
 
 
def initClientsByLegalDetailsFormData(request):

	if not request.GET.get('clientId'):
		clientId = ''
	else:
		clientId = request.GET.get('clientId')

	
	if not request.GET.get('city'):
		city = ''
	else:
		city = request.GET.get('city')
	

	if not request.GET.get('address'):
		address = ''
	else:
		address = request.GET.get('address')

	
	if not request.GET.get('company_name'):
		company_name = ''
	else:
		company_name = request.GET.get('company_name')
	
	

	initial_data = {
					'clientId': clientId,
					'city': city,
					'address': address,
					'company_name': company_name,
					}
	
	return initial_data
 
 
def replace_special_symbols_str(str):
	#print str

	
	str = str.replace("\\", "\\\\")
	#str = str.replace("\#", "\\#")
	str = str.replace("|", "\\|")
	str = str.replace("(", "\\(")
	str = str.replace(")", "\\)")
	str = str.replace("[", "\\[")
	str = str.replace("]", "\\]")
	str = str.replace("{", "\\{")
	str =str.replace("}", "\\}")
	str = str.replace("^", "\\^")
	str = str.replace("$", "\\$")
	str = str.replace("+", "\\+")
	str = str.replace(".", "\\.")
	
	str = str.replace("?", '.')
	str = str.replace("*", ".*")
	str = "^" + str + "$"
	#print str
	return str
	
	
def check_telephoneNum(telephoneNum):
	
	persons = Persons.objects.filter(telephoneNum1 = telephoneNum)
	if len(persons):
		return persons

	persons = Persons.objects.filter(telephoneNum2 = telephoneNum)
	if len(persons):
		return persons
		
	persons = Persons.objects.filter(telephoneNum3 = telephoneNum)
	if len(persons):
		return persons
	
																																

	
def check_email(email):
	
	persons = Persons.objects.filter(email1 = email)
	if len(persons):
		return persons

	persons = Persons.objects.filter(email2 = email)
	if len(persons):
		return persons
		
		
		
# getting clients according to persons search criterias
def get_clients_by_persons_search_criteria(request):

	persons = Persons.objects.all().order_by('-changedOn')

	#search string for firstName
	if request.GET.get('firstName'):
		search_firstName_str = request.GET.get('firstName')
		search_firstName_str = replace_special_symbols_str(search_firstName_str)
		persons = persons.filter(firstName__iregex = search_firstName_str)
		

	#search string for lastName
	if request.GET.get('lastName'):
		search_lastName_str = request.GET.get('lastName')
		search_lastName_str = replace_special_symbols_str(search_lastName_str)
		persons = persons.filter(lastName__iregex = search_lastName_str)
		
	
	#search string for telephoneNum1
	if request.GET.get('telephoneNum'):
		search_telephoneNum_str = request.GET.get('telephoneNum')
		search_telephoneNum_str = replace_special_symbols_str(search_telephoneNum_str)
		persons = persons.filter(Q(telephoneNum1__iregex = search_telephoneNum_str)|Q(telephoneNum2__iregex = search_telephoneNum_str)|Q(telephoneNum3__iregex = search_telephoneNum_str))
		
	#search string for email
	if request.GET.get('email'):
		search_email_str = request.GET.get('email')
		search_email_str = replace_special_symbols_str(search_email_str)
		persons = persons.filter(Q(email1__iregex = search_email_str)|Q(email2__iregex = search_email_str))

	return persons
	
	
	
	

# getting clients according to LK search criterias
def get_clients_by_LK_search_criteria(request):

	LKs = LK.objects.all().order_by('-changedOn')

	#search string for client id
	if request.GET.get('clientId'):
		search_clientId_str = request.GET.get('clientId')
		search_clientId_str = replace_special_symbols_str(search_clientId_str)
		LKs = LKs.filter(client__id__iregex = search_clientId_str) 

	#search string for LK
	if request.GET.get('LK'):
		search_LK_str = request.GET.get('LK')
		search_LK_str = replace_special_symbols_str(search_LK_str)
		LKs = LKs.filter(LK__iregex = search_LK_str)

	return LKs
	



# getting clients according to legal details search criterias
def get_clients_by_legal_details_search_criteria(request):

	legal_details = Legal_details.objects.all().order_by('-changedOn')

	#search string for client id
	if request.GET.get('clientId'):
		search_clientId_str = request.GET.get('clientId')
		search_clientId_str = replace_special_symbols_str(search_clientId_str)
		legal_details = legal_details.filter(client__id__iregex = search_clientId_str) 

	#search string for city
	if request.GET.get('city'):
		search_city_str = request.GET.get('city')
		search_city_str = replace_special_symbols_str(search_city_str)
		legal_details = legal_details.filter(city__iregex = search_city_str)


	#search string for address
	if request.GET.get('address'):
		search_address_str = request.GET.get('address')
		search_address_str = replace_special_symbols_str(search_address_str)
		legal_details = legal_details.filter(address__iregex = search_address_str)


	#search string for company_name
	if request.GET.get('company_name'):
		search_company_name_str = request.GET.get('company_name')
		search_company_name_str = replace_special_symbols_str(search_company_name_str)
		legal_details = legal_details.filter(company_name__iregex = search_company_name_str)

	return legal_details




	
	
def get_status_numbers(**kwargs):
	request = kwargs.get('request')
	
	if not request:
		orders = Order.objects.all()
	
		count = orders.filter(status='INTS').count()
		if not count:
			count = 0
		status_numbers = {'INTS':count}
	
	
		count = orders.filter(status='EVAL').count()
		if not count:
			count = 0
		status_numbers.update({'EVAL':count})
	
	
		
		count = orders.filter(status='OFER').count()
		if not count:
			count = 0
		status_numbers.update({'OFER':count})
	
		
		count = orders.filter(status='WAIT').count()
		if not count:
			count = 0
		status_numbers.update({'WAIT':count})
	
		
		count = orders.filter(status='DVLR').count()
		if not count:
			count = 0
		status_numbers.update({'DVLR':count})
		
	
		count = orders.filter(status='PROC').count()
		if not count:
			count = 0
		status_numbers.update({'PROC':count})
		
		count = orders.filter(status='DONE').count()
		if not count:
			count = 0
		status_numbers.update({'DONE':count})
		
		count = orders.filter(status='FAIL').count()
		if not count:
			count = 0
		status_numbers.update({'FAIL':count})
	
	else:
		orders = Order_process.objects.filter(step=1)
	
	
		#search string for client id
		if request.GET.get('clientId'):
			search_clientId_str = request.GET.get('clientId')
			search_clientId_str = replace_special_symbols_str(search_clientId_str)
			orders = orders.filter(order__client__id__iregex = search_clientId_str) 
	
	
	
		#searxch string for orderId
		if request.GET.get('orderId'):
			search_orderId_str = request.GET.get('orderId')
			search_orderId_str = replace_special_symbols_str(search_orderId_str)
			orders = orders.filter(order__id__iregex = search_orderId_str) 
	
	
	
	
		#search string for firstName
		if request.GET.get('firstName'):
			search_firstName_str = request.GET.get('firstName')
			search_firstName_str = replace_special_symbols_str(search_firstName_str)
			orders = orders.filter(order__contactPerson__firstName__iregex = search_firstName_str)
	
			
		#search string for telephoneNum1
		if request.GET.get('telephoneNum1'):
			search_telephoneNum1_str = request.GET.get('telephoneNum1')
			search_telephoneNum1_str = replace_special_symbols_str(search_telephoneNum1_str)
			orders = orders.filter(order__contactPerson__telephoneNum1__iregex = search_telephoneNum1_str)
	
	
		#search string for email1
		if request.GET.get('email1'):
			search_email1_str = request.GET.get('email1')
			search_email1_str = replace_special_symbols_str(search_email1_str)
			orders = orders.filter(order__contactPerson__email1__iregex = search_email1_str)
	
	
	
	
	
		#search string for step_description
		if request.GET.get('step_description'):
			search_step_description_str = request.GET.get('step_description')
			search_step_description_str = replace_special_symbols_str(search_step_description_str)
			orders = orders.filter(step_description__iregex = search_step_description_str)
			
	
	
	
		#search string for manager
		if request.GET.get('manager') != "all" and request.GET.get('manager') != None:
				orders = orders.filter(order__manager__username = request.GET.get('manager'))
				
				
		#search string for call_or_email
		if request.GET.get('call_or_email') != "all" and request.GET.get('call_or_email') != None:
				orders = orders.filter(order__call_or_email = request.GET.get('call_or_email'))
				#print request.GET.get('call_or_email')
				
	
		#search for orderDate
		if request.GET.get('orderDateBegin') \
			and request.GET.get('orderDateEnd') \
			and request.GET.get('orderDateBegin') != 'None' \
			and request.GET.get('orderDateEnd') != 'None':
			
				#make some transformation beacause last date is condering by django as date and 00:00:00 time
				orderDateEnd = datetime.strptime(request.GET.get('orderDateEnd'), "%Y-%m-%d") + timedelta(days=1)
			
				orders = orders.filter(date_step__range=(request.GET.get('orderDateBegin'), orderDateEnd))
	
	
		#search for call_on
		if request.GET.get('call_onBegin') \
			and request.GET.get('call_onEnd') \
			and request.GET.get('call_onBegin') != 'None' \
			and request.GET.get('call_onEnd') != 'None':
			
				
				call_onEnd = datetime.strptime(request.GET.get('call_onEnd'), "%Y-%m-%d")
			
				orders = orders.filter(order__call_on__range=(request.GET.get('call_onBegin'), call_onEnd))
			
			

		count = orders.filter(order__status='INTS').count()
		if not count:
			count = 0
		status_numbers = {'INTS':count}
	
	
		count = orders.filter(order__status='EVAL').count()
		if not count:
			count = 0
		status_numbers.update({'EVAL':count})
	
	
		
		count = orders.filter(order__status='OFER').count()
		if not count:
			count = 0
		status_numbers.update({'OFER':count})
	
		
		count = orders.filter(order__status='WAIT').count()
		if not count:
			count = 0
		status_numbers.update({'WAIT':count})
	
		
		count = orders.filter(order__status='DVLR').count()
		if not count:
			count = 0
		status_numbers.update({'DVLR':count})
		
	
		count = orders.filter(order__status='PROC').count()
		if not count:
			count = 0
		status_numbers.update({'PROC':count})
		
		count = orders.filter(order__status='DONE').count()
		if not count:
			count = 0
		status_numbers.update({'DONE':count})
		
		count = orders.filter(order__status='FAIL').count()
		if not count:
			count = 0
		status_numbers.update({'FAIL':count})
	
	
	total_number = ( status_numbers.get('INTS') \
					+ status_numbers.get('EVAL') \
					+ status_numbers.get('OFER') \
					+ status_numbers.get('WAIT') \
					+ status_numbers.get('DVLR') \
					+ status_numbers.get('PROC') \
					+ status_numbers.get('DONE') \
					+ status_numbers.get('FAIL') \
					)
	status_numbers.update({'total_number': total_number})
	
	return status_numbers
	
	
def get_week_analytics():
	day = datetime.today()
	struct_datetime = day.timetuple()
	count = Order_process.objects.filter(date_step__day=struct_datetime[2], date_step__month=struct_datetime[1], date_step__year=struct_datetime[0], step=1).count()
	week_analytics_l = [(day.date(), count)]
	
	
	for i in range(6):
		day = day-timedelta(days=1)
		struct_datetime = day.timetuple()
		count = Order_process.objects.filter(date_step__day=struct_datetime[2], date_step__month=struct_datetime[1], date_step__year=struct_datetime[0], step=1).count()
		week_analytics_l.append((day.date(), count))
	
	return week_analytics_l







def iterate_by_date(request):
	
	###################
	#check out date begin and date end parameters
	if request.GET.get('orderDateBegin') == None:
		orderDateBegin = str(datetime.date(datetime.today() - timedelta(days=7)))
	else:
		orderDateBegin = request.GET.get('orderDateBegin')
	
	if request.GET.get('orderDateEnd') == None:
		orderDateEnd = str(date.today())
	else:
		orderDateEnd = request.GET.get('orderDateEnd')
	
	orderDateBegin = datetime.strptime(orderDateBegin, "%Y-%m-%d")
	orderDateEnd = datetime.strptime(orderDateEnd, "%Y-%m-%d")


	###################
	#prepare Query sets
	#make some transformation beacause last date is condering by django as date and 00:00:00 time
	orderDateEnd1 = orderDateEnd + timedelta(days=1)
	
	Glazok_orders = Order_process.objects.filter(step=1, order__call_or_email = 'Glazok', date_step__range=(orderDateBegin, orderDateEnd1))
	Manggis_orders = Order_process.objects.filter(step=1, order__call_or_email = 'Manggis', date_step__range=(orderDateBegin, orderDateEnd1))

	if request.GET.get('status') != "all" and request.GET.get('status') != None:
			Glazok_orders = Glazok_orders.filter(order__status = request.GET.get('status'))
			Manggis_orders = Manggis_orders.filter(order__status = request.GET.get('status'))

	
	if request.GET.get('manager') != "all" and request.GET.get('manager') != None:
			Glazok_orders = Glazok_orders.filter(order__manager__username = request.GET.get('manager'))
			Manggis_orders = Manggis_orders.filter(order__manager__username = request.GET.get('manager'))




	######################
	#create list of order numbers using group by
	order_numbers = []
	if request.GET.get('group_by') == 'DAY' \
		or request.GET.get('group_by') == None:
			day = orderDateBegin
			while day<=orderDateEnd: 

				Glazok_numbers = Glazok_orders.filter(date_step__date=day).count()
				Glazok_numbers_DONE = Glazok_orders.filter(date_step__date=day, order__status = 'DONE').count()
				Glazok_numbers_FAIL = Glazok_orders.filter(date_step__date=day, order__status = 'FAIL').count()
				Manggis_numbers = Manggis_orders.filter(date_step__date=day).count()
				Manggis_numbers_DONE =  Manggis_orders.filter(date_step__date=day, order__status = 'DONE').count()
				Manggis_numbers_FAIL =  Manggis_orders.filter(date_step__date=day, order__status = 'FAIL').count()
				total = Glazok_numbers + Manggis_numbers 
				orderDateBegin_link = day
				orderDateEnd_link = day
				order_numbers.append((orderDateBegin_link, 
										Glazok_numbers, 
										Manggis_numbers, 
										Glazok_numbers_DONE, 
										Glazok_numbers_FAIL, 
										Manggis_numbers_DONE, 
										Manggis_numbers_FAIL,
										total,
											orderDateEnd_link,
											))
				day = day + timedelta(days=1)

				

	elif request.GET.get('group_by') == 'MONTH':
			#month = datetime.date(orderDateBegin).month
			#month_end = datetime.date(orderDateEnd).month
			#while month<=month_end:
				#Glazok_numbers = Glazok_orders.filter(date_step__month=month).count()
				#Glazok_numbers_DONE = Glazok_orders.filter(date_step__month=month, order__status = 'DONE').count()
				#Glazok_numbers_FAIL = Glazok_orders.filter(date_step__month=month, order__status = 'FAIL').count()
				#Manggis_numbers = Manggis_orders.filter(date_step__month=month).count()
				#Manggis_numbers_DONE =  Manggis_orders.filter(date_step__month=month, order__status = 'DONE').count()
				#Manggis_numbers_FAIL =  Manggis_orders.filter(date_step__month=month, order__status = 'FAIL').count()
				#date_begin_link, date_end_link = set_begin_n_end_day_for_period(request.GET.get('group_by'))
				#total = Glazok_numbers + Manggis_numbers 
				#order_numbers.append((month, Glazok_numbers, Manggis_numbers, 
											#Glazok_numbers_DONE, Glazok_numbers_FAIL, 
											#Manggis_numbers_DONE, Manggis_numbers_FAIL,
											#total))
				#month = month + 1
				#debug
			day = datetime(orderDateBegin.year, orderDateBegin.month, 1)
			while day<=orderDateEnd: 
				if day < orderDateBegin:
					orderDateBegin_link = orderDateBegin
				else:
					orderDateBegin_link = day
				
				orderDateEnd_link = day + timedelta(days=(monthrange(day.year, day.month)[1] - 1))
				if orderDateEnd_link > orderDateEnd:
					orderDateEnd_link = orderDateEnd
								
				#print 'begin:', orderDateBegin_link, "end:", orderDateEnd_link 
				Glazok_numbers = Glazok_orders.filter(date_step__range=(orderDateBegin_link, orderDateEnd_link)).count()
				Glazok_numbers_DONE = Glazok_orders.filter(date_step__range=(orderDateBegin_link, orderDateEnd_link), order__status = 'DONE').count()
				Glazok_numbers_FAIL = Glazok_orders.filter(date_step__range=(orderDateBegin_link, orderDateEnd_link), order__status = 'FAIL').count()
				Manggis_numbers = Manggis_orders.filter(date_step__range=(orderDateBegin_link, orderDateEnd_link)).count()
				Manggis_numbers_DONE =  Manggis_orders.filter(date_step__range=(orderDateBegin_link, orderDateEnd_link), order__status = 'DONE').count()
				Manggis_numbers_FAIL =  Manggis_orders.filter(date_step__range=(orderDateBegin_link, orderDateEnd_link), order__status = 'FAIL').count()
				total = Glazok_numbers + Manggis_numbers 
				order_numbers.append((orderDateBegin_link, 
												Glazok_numbers, 
												Manggis_numbers, 
												Glazok_numbers_DONE, 
												Glazok_numbers_FAIL, 
												Manggis_numbers_DONE, 
												Manggis_numbers_FAIL,
												total,
												orderDateEnd_link
												))
				day = day + timedelta(days=monthrange(day.year, day.month)[1])
				#print 'day', day
				#print

			
	elif request.GET.get('group_by') == 'YEAR':
			year = datetime.date(orderDateBegin).year
			year_end = datetime.date(orderDateEnd).year
			while year<=year_end:
				orderDateBegin_link = datetime(year, 1, 1)
				orderDateEnd_link = datetime(year, 12, 31)
				
				if orderDateBegin_link < orderDateBegin:
					orderDateBegin_link = orderDateBegin
					
				if orderDateEnd_link > orderDateEnd:
					orderDateEnd_link = orderDateEnd 
				
				#print "begin:", orderDateBegin_link, "end:", orderDateEnd_link 
				#print
				
				Glazok_numbers = Glazok_orders.filter(date_step__year=year).count()
				Glazok_numbers_DONE = Glazok_orders.filter(date_step__year=year, order__status = 'DONE').count()
				Glazok_numbers_FAIL = Glazok_orders.filter(date_step__year=year, order__status = 'FAIL').count()
				Manggis_numbers = Manggis_orders.filter(date_step__year=year).count()
				Manggis_numbers_DONE =  Manggis_orders.filter(date_step__year=year, order__status = 'DONE').count()
				Manggis_numbers_FAIL =  Manggis_orders.filter(date_step__year=year, order__status = 'FAIL').count()
				total = Glazok_numbers + Manggis_numbers 
				order_numbers.append((orderDateBegin_link,
										Glazok_numbers, 
										Manggis_numbers, 
										Glazok_numbers_DONE, 
										Glazok_numbers_FAIL, 
										Manggis_numbers_DONE, 
										Manggis_numbers_FAIL,
										total,
										orderDateEnd_link,
										))
				year = year + 1
	else:
			print 'what else?'
	


	
	
	return order_numbers
	
	
	









def init_data_for_orders_report(request):




	if request.GET.get('orderDateBegin') == None:
		orderDateBegin = str(datetime.date(datetime.today() - timedelta(days=7)))

	else:
		orderDateBegin = request.GET.get('orderDateBegin')
	

	if request.GET.get('orderDateEnd') == None:
		orderDateEnd = str(date.today())
	else:
		orderDateEnd = request.GET.get('orderDateEnd')
	


	if request.GET.get('status') == None:
		status = 'all'
	else:
		status = request.GET.get('status')
		
		
					
	if request.GET.get('manager') == None:
		manager = 'all'
	else:
		manager = request.GET.get('manager')
					


	if request.GET.get('group_by') == None:
		group_by = 'DAY'
	else:
		group_by = request.GET.get('group_by')					
					
					
	initial_data = {
					'manager': manager, 
					'group_by': group_by, 
					'status': status, 
					'orderDateBegin': orderDateBegin, 
					'orderDateEnd': orderDateEnd, 
					}
	return initial_data






#def set_begin_n_end_day_for_period(period_type):
	
	
	#date_end = '2001-12-01'
	#date_begin = '2001-12-01'
	
	##if period_type == "MONTH":
		##date_begin = "2017-" + "04-" + str(monthrange(2017, 04)[1])
		##print period_type
	
	#return date_begin, date_end
















