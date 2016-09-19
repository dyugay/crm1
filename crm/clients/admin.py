from django.contrib import admin

# Register your models here.
from clients.models import Order, Order_process, Client, ClientContactDetails
from clients.models import Legal_details
#, Account, Billing

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'client')
	
class ClientAdmin(admin.ModelAdmin):
	list_display = ('id', 'author')
	
	
class Legal_detailsAdmin(admin.ModelAdmin):
	list_display = ('id', 'city')

admin.site.register(Order, OrderAdmin)
admin.site.register(Order_process)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientContactDetails)
admin.site.register(Legal_details, Legal_detailsAdmin)
#admin.site.register(Account)
#admin.site.register(Billing)



