from django.contrib import admin

from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Wilaya, Commune, Order, OrderItem
import csv
import datetime

class WilayaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','price', 'active')
    list_display_links = ('id', 'name',)
    list_per_page = 20
    list_filter = ('price', 'active',)
    list_editable = ('active',)
    search_fields = ('name',)

# class WilayaItemInline(admin.TabularInline):
#     model = Wilaya
#     raw_id_fields = ['wilaya']

# class CommuneItemInline(admin.TabularInline):
#     model = Commune
#     raw_id_fields = ['commune']

class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    raw_id_fields   = ['product', ]
    
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'wilaya')
    list_display_links = ('id',)
    list_per_page = 20
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name', 'phone','email', 'created', 'updated', 'paid','confirmed')
    list_display_links = ('id',)
    list_per_page = 40
    list_filter = ('paid', 'created', 'updated', 'wilaya', 'commune')
    list_editable = ('paid','confirmed')
    search_fields = ('id', 'last_name','phone', 'email') 
    inlines = [OrderItemInline]
    #actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)
admin.site.register(Wilaya, WilayaAdmin)
admin.site.register(Commune, CommuneAdmin)

