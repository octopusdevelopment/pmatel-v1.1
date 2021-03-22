
from django.contrib import admin
from django.urls import path
from .views import Home, AboutView, ContactView, SolutionView, \
                    SolutionDetailView, CatalogView, ProductDetailsView, \
                    ProductByCategoryView, SearchCatalogView, SearchProductView, \
                    ProductNameAscView, ProductNameDescView, ProductPriceAscView, ProductPriceDescView, \
                    ProductPromotionView, ContactFormView


urlpatterns = [
    path('', Home.as_view(), name= 'index'),
    #About
    path('about/', AboutView.as_view(), name= 'about'),

    # Products 
    path('produits/resultats-recherche', SearchCatalogView.as_view(), name='product-search'),
    path('produits/promotion', ProductPromotionView.as_view(), name='product-promotion'),
    path('produits/resultats-de-la-recherche', SearchProductView.as_view(), name='product-search-advanced'),
    path('produits/ordonnes-par-nom-croissant/', ProductNameAscView.as_view(), name='product-name-asc'),
    path('produits/ordonnes-par-nom-decroissant/', ProductNameDescView.as_view(), name='product-name-desc'),
    path('produits/ordonnes-par-prix-croissant/', ProductPriceAscView.as_view(), name='product-price-asc'),
    path('produits/ordonnes-par-prix-decroissant/', ProductPriceDescView.as_view(), name='product-price-desc'),
    path('produits/', CatalogView.as_view(), name= 'produits'),
    path('produits/<slug:slug>/', ProductDetailsView.as_view(), name='product-details'),
    path('produits/category/<slug:category_slug>/', ProductByCategoryView.as_view(), name='product-by-cat'),
   
    
    
    #path('rechercher-produits/<>')
    # Solution
    path('solution/', SolutionView.as_view(), name= 'solution'),
    path('solution/<slug:slug>/', SolutionDetailView.as_view(), name= 'produit'),

    
    #Contact
    path('contact/', ContactView.as_view(), name= 'contact'),
    path('contact/send/', ContactFormView.as_view(), name= 'contact-send'),
    
]

