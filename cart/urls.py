from django.urls import path
from . import views
app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('ajouter/<int:product_id>/', views.cart_add, name='cart_add'),
    path('ajouter-au-panier<int:product_id>/', views.cart_add_one_product, name='cart_add_one_product'),
    path('ajouter-au-panier/<slug:slug>/<int:product_id>/', views.cart_add_one_product_with_quantity, name='cart_add_one_product_with_quantity'),
    path('modifier/<int:product_id>/', views.cart_update_with_json, name='cart_update'),
    path('supprimer/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('vider/', views.cart_empty, name='cart_empty'),
]