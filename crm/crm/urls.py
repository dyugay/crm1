# -*- coding: utf-8 -*-
"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from clients.views import main, createOrder, order, createPerson
from clients.views import loginUser, logoutUser, get_orders_list
from clients.views import client, changePerson, addLK, changeClientLK, addLegalDetails
from clients.views import changeLegalDetails, createClient, get_clients_by_persons, get_clients_by_LK
from clients.views import get_clients_by_legal_details, reports, report_orders
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', main, name='main'),
	url(r'^new_order/(?P<clientId>\d+)*/*$', createOrder, name='createOrder'),
	url(r'^order/(?P<orderId>\d+)*/*$', order, name='order'),
	url(r'^login/.*$', loginUser, name='loginUser'),
	url(r'^logout/.*$', logoutUser, name='logoutUser'),
	url(r'^orders_list/(?P<pageNum>\d+)*/*/$', get_orders_list, name = 'get_orders_list'),
	url(r'^client/(?P<clientId>\d+)*/*$', client, name="client"),
	url(r'^new_client/$', createClient, name="createClient"),
	url(r'^new_person/(?P<clientId>\d+)*/*$', createPerson, name='createPerson'),
	url(r'^person/(?P<personId>\d+)*/*$', changePerson, name='changePerson'),
	url(r'^new_LK/(?P<clientId>\d+)*/*$', addLK, name='addLK'),
	url(r'^changeClientLK/(?P<LK_Id>\d+)*/*$', changeClientLK, name='changeClientLK'),
	url(r'^addLegalDetails/(?P<clientId>\d+)*/*$', addLegalDetails, name='addLegalDetails'),
	url(r'^changeLegalDetails/(?P<legal_details_id>\d+)*/*$', changeLegalDetails, name='changeLegalDetails'),
	url(r'^clients_by_persons/(?P<pageNum>\d+)*/*$', get_clients_by_persons, name='get_clients_by_persons'),
	url(r'^clients_by_LK/(?P<pageNum>\d+)*/*$', get_clients_by_LK, name='get_clients_by_LK'),
	url(r'^clients_by_legal_details/(?P<pageNum>\d+)*/*$', get_clients_by_legal_details, name='get_clients_by_legal_details'),
	url(r'^reports/.*$', reports, name='reports'),
	url(r'^report_orders/(?P<pageNum>\d+)*/*/$', report_orders, name='report_orders'),


] 

urlpatterns += staticfiles_urlpatterns()
