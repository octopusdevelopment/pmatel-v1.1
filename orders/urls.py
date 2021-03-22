from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('modifier-quantite/', views.order_update_quantity, name='order_update_quantity'),
    path('ajouter-coupon/', views.order_apply_coupon, name='order_apply_coupon'),
    
    path('creer-commande/', views.order_create, name='order_create'),
    path('creer-commande/<int:product_id>', views.order_create_one_product, name='order_create_one_product'),
    
    path('fetch/load-communes/', views.load_communes_json, name='load_communes_fetch'),
    path('fetch/load-wilaya/', views.load_wilaya_json, name='load_wilaya_fetch'),
    
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf')
]