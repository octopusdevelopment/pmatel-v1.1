from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import ContactForm, Solution, Product, Category
#forms 
from .forms import ContactForm, SearchForm, HomeProductSeachForm
from cart.forms import CartAddProductForm
# pagination
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
#search
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
# shuffle elements catalogue
import random


class Home(TemplateView):
    template_name='main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SearchProductView(ListView):
    template_name = 'main/shop.html'
    context_object_name = 'product'
    model = Product
    paginate_by = 24
    
    form = HomeProductSeachForm()    
    def get_queryset(self):
        
        self.products = []
            
        form = HomeProductSeachForm(self.request.GET)

        if form.is_valid():
            product = form.cleaned_data['product']
            try:
                print('LENGTH',len(product))
            except:
                product = ""
            try:
                category = self.request.GET['category'][0]
                len(category)
            except:
                category=''
            try:
                status = self.request.GET['status'][0]
                len(status)
            except:
                status = ''
                
            search_vector = SearchVector('name', config='french', weight='A') + SearchVector('description', config='french', weight='B')
            search_query = SearchQuery(product)    
            if ( len(product) & len(status) & len(category)):
                query_products = Product.show.filter(status = status, category__id=category).annotate(search= search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            elif(len(product) & len(status)):
                query_products = Product.show.filter(status = status).annotate(search= search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            elif(len(product) & len(category)):
                query_products = Product.show.filter(category__id=category).annotate(search= search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            elif(len(status) & len(category)):
                query_products = Product.show.filter(status = status, category__id=category) 
            elif len(product):
                query_products = Product.show.annotate(search= search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
                print("INSIDE PRODUCT")
            elif len(status):
                query_products = Product.show.filter(status = status) 
            elif len(category):
                query_products = Product.show.filter(category__id = category)
            else:
                query_products = Product.show.all()
            self.products = query_products
        return self.products 
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        products = self.products

        print(products)
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        return context  
    
class AboutView(TemplateView):
    template_name = "other/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solutions"] = Solution.objects.all()
        return context

class SolutionDetailView(ListView):
    model = Product
    template_name = "solution-details.html"
    context_object_name = 'solution'

    def get_queryset(self):
        self.solution = get_object_or_404(Solution, slug=self.kwargs['slug'])
        return self.solution
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["produits"] = Product.objects.filter(solution=self.solution)
        context["solutions"] = Solution.objects.all()
        return context


class SolutionView(TemplateView):
    template_name = "solution.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solutions"] = Solution.objects.all()
        return context


class CatalogView(ListView):
    template_name = 'main/shop.html'
    context_object_name = 'product'
    model = Product
    paginate_by = 24
    
    def get_queryset(self):
        self.products = Product.objects.filter(available=True, stock__gte=1)
        return self.products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        return context    

class SearchCatalogView(ListView):
    template_name = 'main/shop.html'
    context_object_name = 'product'
    model = Product
    paginate_by = 24
    
    form = SearchForm()
    query = None
    
    def get_queryset(self):
        
        self.products = []
        if 'query' in self.request.GET:
            
            form = SearchForm(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']     
                search_vector = SearchVector('name', config='french', weight='A') + SearchVector('description', config='french', weight='B')
                search_query = SearchQuery(query)
                self.products = Product.show.annotate(search= search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
                
        return self.products
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        products = self.products
        
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        return context    

class ProductDetailsView(ListView):
    model = Product
    template_name='main/product-detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        self.product = get_object_or_404(Product, slug=self.kwargs['slug'], stock__gte=1, available=True)
        self.similar_products =sorted(Product.objects.filter(category= self.product.category, stock__gte=1, available=True).exclude(slug=self.kwargs['slug'])[:4], key=lambda x: random.random())
        return self.product
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        context["similar_products"] = self.similar_products
        # self.similar_products = list(self.similar_products)
        # self.similar_products = shuffle(self.similar_products)
        print(self.similar_products, "similar PRODUCTS")
        # if (self.similar_products):
        #     if(len(self.similar_products)<4):
        #         context["similar_products"] = self.similar_products
        #     else:
        #         context["similar_products"] = self.similar_products[0:4]
        return context


class ProductByCategoryView(ListView):
    model = Product
    template_name= 'main/shop.html'
    paginate_by = 24
    def get_queryset(self):
        
        self.category = get_object_or_404(Category, slug = self.kwargs['category_slug'])
        self.products = Product.objects.filter(category = self.category, available=True, stock__gte=1)
        return self.products
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        context["category"] = self.category
        return context

class ProductNameAscView(ListView):
    model = Product
    template_name= 'main/shop.html'
    paginate_by = 24
    def get_queryset(self):
        
        self.products = Product.show.all().order_by('name')
        return self.products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        context["category"] = "Tous les produits"
        return context

class ProductNameDescView(ListView):
    model = Product
    template_name= 'main/shop.html'
    paginate_by = 24
    def get_queryset(self):
        
        self.products = Product.show.all().order_by('-name')
        return self.products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        context["category"] = "Tous les produits"
        return context    

class ProductPriceAscView(ListView):
    model = Product
    template_name= 'main/shop.html'
    paginate_by = 24
    def get_queryset(self):
        self.products = Product.show.all().order_by('price')
        return self.products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        context["category"] = "Tous les produits"
        return context

class ProductPriceDescView(ListView):
    model = Product
    template_name= 'main/shop.html'
    paginate_by = 24
    def get_queryset(self):
        
        self.products = Product.show.all().order_by('-price')
        return self.products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        context["category"] = "Tous les produits"
        return context  

class ContactView(TemplateView):
    template_name = "other/contact.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class ContactFormView(CreateView):
    template_name = 'other/contact.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        message = 'Une erreur est survenue, veuillez réessayer.'
        success = False
        try:
            #save the form   
            if form.is_valid():
                form.save()

                #messages.success(request, 'Votre message a bien été envoyé')
                message = 'Votre message a bien été envoyé!'
                success = True
                print(success)
                return render(request, 'other/contact.html', {'message': message, 'success': success})
            else:
                #print(form.errors)
                #messages.error(request, 'Vérifier vos données et réessayez')
                print(success)
                message = 'Une erreur est survenue, veuillez réessayer.'

                return render(request, 'other/contact.html', {'message': message, 'failure': True})
        except:
            return render(request, 'other/contact.html', {'message': message, 'failure': True})
        return render(request, 'other/contact.html', {'message': message, 'failure': True})


class ProductPromotionView(ListView):
    model = Product
    template_name= 'main/shop.html'
    paginate_by = 24
    def get_queryset(self):
        
        self.products = Product.show.filter(status='P')
        return self.products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)
        context["products"] = list_products
        context["category"] = "Tous les produits"
        return context   