from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount_percentage', 'discount_amount', 'active', 'stock']
    list_filter = ['active', 'valid_from', 'valid_to']
    list_editable = ['valid_from', 'valid_to', 'discount_percentage', 'discount_amount', 'active', 'stock']
    search_fields = ['code']