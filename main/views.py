from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ContactForm
from .models import ContactForm, Solution, Product, Category

from cart.forms import CartAddProductForm

class Home(TemplateView):
    template_name='index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solutions'] = Solution.objects.all()
        return context
    
class AboutView(TemplateView):
    template_name = "about.html"

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

class CatalogView(TemplateView):
    template_name = 'catalog.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(available = True, stock__gte=1)
        return context    

class ProductDetailsView(ListView):
    model = Product
    template_name='product-details.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        self.product = get_object_or_404(Product, slug=self.kwargs['slug'], stock__gte=1)
        return self.product
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context["cart_product_form"] = cart_product_form
        context["produits"] = self.product
        return context


class ProductByCategoryView(ListView):
    model = Category
    template_name='catalog.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        
        self.category = get_object_or_404(Category, slug = self.kwargs['category_slug'])
        self.products = Product.objects.filter(category = self.category, available= True, stock__gte=1)
        return self.products
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.products
        return context
    

class ContactView(TemplateView):
    template_name = "contact.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class ContactFormView(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        # form = self.get_form()
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Votre message a bien été envoyer')
        else:
            print(form.errors)
            messages.error(request, 'Vérifier vos données et réessayer')
        return redirect('/contact')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solutions"] = Solution.objects.all()
        return context
