
from django.contrib import admin
from django.urls import path
from .views import Home, AboutView, ContactView, SolutionView, \
                    SolutionDetailView, CatalogView, ProductDetailsView


urlpatterns = [
    path('', Home.as_view(), name= 'index'),
    path('about/', AboutView.as_view(), name= 'about'),
    path('produits/', CatalogView.as_view(), name= 'produits'),
    path('produits/<slug:slug>/', ProductDetailsView.as_view(), name='details-produit'),
    path('solution/', SolutionView.as_view(), name= 'solution'),
    path('solution/<slug:slug>/', SolutionDetailView.as_view(), name= 'produit'),
    
    path('contact/', ContactView.as_view(), name= 'contact'),
    
]

