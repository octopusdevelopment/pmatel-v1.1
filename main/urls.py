
from django.contrib import admin
from django.urls import path
from .views import Home, AboutView, ContactView, SolutionView, \
                    SolutionDetailView, CatalogView, ProductDetailsView, \
                    ProductByCategoryView


urlpatterns = [
    path('', Home.as_view(), name= 'index'),
    #About
    path('about/', AboutView.as_view(), name= 'about'),

    # Products 
    path('produits/', CatalogView.as_view(), name= 'produits'),
    path('produits/<slug:slug>/', ProductDetailsView.as_view(), name='details-produit'),
    path('produits/category/<slug:category_slug>/', ProductByCategoryView.as_view(), name='product-by-cat'),

    # Solution
    path('solution/', SolutionView.as_view(), name= 'solution'),
    path('solution/<slug:slug>/', SolutionDetailView.as_view(), name= 'produit'),

    
    #Contact
    path('contact/', ContactView.as_view(), name= 'contact'),
    
]

