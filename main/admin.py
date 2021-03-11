from django.contrib import admin
from .models import Product, Solution, Category

admin.autodiscover()
admin.site.enable_nav_sidebar = False



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','name', 'category','price','stock', 'status', 'available')
    prepopulated_fields = {"slug": ("name","product_id")}
    list_display_links = ('product_id',)
    list_per_page = 40
    list_filter = ('name', 'category',)
    list_editable = ['price', 'available', 'name', 'status','stock']
    search_fields = ('name','product_id',)
    exlude = ['slug']


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id',)
    list_per_page = 40
    list_filter = ('name',)
    list_editable = ['description',]
    search_fields = ('id', 'name')
    exlude = ['slug']
 



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id',)
    list_per_page = 40
    list_filter = ('name',)
    list_editable = ['name']
    search_fields = ('id', 'name',)
    exlude = ['slug']

admin.site.register(Product, ProductAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Category, CategoryAdmin)
