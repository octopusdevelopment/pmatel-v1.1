
from django.contrib import admin
from django.urls import path
from .views import Home, AboutView, ContactView
#  , CatalogueListView, SolutionView, SolutionDetail, ContactFormView, PartenaireView, GammeDetailList, BlogView, PostDetail
urlpatterns = [
    path('', Home.as_view(), name= 'index'),
    path('about/', AboutView.as_view(), name= 'about'),
    # # path('catalogue/', CatalogueListView.as_view(), name= 'catalogue'),
    # path('produits/', CatalogueListView.as_view(), name= 'produits'),
    # path('solution/', SolutionView.as_view(), name= 'solution'),
    # path('solution/<slug:slug>/', SolutionDetail.as_view(), name= 'solution-detail'),
    # path('actualite/<slug:slug>/', PostDetail.as_view(), name= 'post-detail'),
    path('contact/', ContactView.as_view(), name= 'contact'),
    # path('partenaires/', PartenaireView.as_view(), name= 'partenaires'),
    # path('actualite/', BlogView.as_view(), name= 'blog'),
    # path('produits-<slug:slug>/', GammeDetailList.as_view(), name= 'produit-detail'),
    # path('catalogue/<int:pk>/', GammeDetail.as_view(), name= 'gamme'),
]

