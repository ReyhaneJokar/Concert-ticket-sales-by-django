from django.contrib import admin
from ticketSales.models import concertModel 
from ticketSales.models import locationModel 
from ticketSales.models import timeModel 
from ticketSales.models import ticketModel

# Register your models here.

admin.site.register(concertModel)
admin.site.register(locationModel)
admin.site.register(timeModel)
admin.site.register(ticketModel)
