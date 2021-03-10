from django.contrib import admin

from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Wilaya, Commune, Order, OrderItem
import csv
import datetime


def export_to_csv(modelAdmin, request, queryset):
    opts = modelAdmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response

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

class CommuneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'wilaya')
    list_display_links = ('id',)
    list_per_page = 20
    search_fields = ('name',)
    
    
class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    raw_id_fields   = ['product', ]

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    order_pdf.short_description = 'Facture'
    return mark_safe(f'<a href="{url}">PDF</a>')

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    order_detail.short_description = 'Exporter en CSV'
    return mark_safe(f'<a href="{url}">Voir</a>')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name', 'phone','email', 'created', 'paid','confirmed', order_detail, order_pdf)
    list_display_links = ('id',)
    list_per_page = 40
    list_filter = ('paid', 'created', 'updated', 'wilaya', 'commune')
    list_editable = ('paid','confirmed')
    search_fields = ('id', 'last_name','phone', 'email') 
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)
admin.site.register(Wilaya, WilayaAdmin)
admin.site.register(Commune, CommuneAdmin)

