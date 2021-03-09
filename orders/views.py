from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse


from .models import OrderItem, Wilaya, Commune, Order
from main.models import Product
from cart.cart import Cart
from .forms import OrderCreateForm

from django.conf import settings
import json
from django.core import serializers

def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    wilayas = Wilaya.objects.all()
    
    if request.method == 'POST':
        if len(cart):
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                cart.clear()
                #order_created.delay(order.id)
                return render(request, 'order_created.html', {'order': order})
        else:
            return redirect(request, 'catalog.html')
    else:
        form = OrderCreateForm()
    
    return render(request, 'order.html', {'cart':cart, 'form' : form, 'wilayas': wilayas})



def order_create_one_product(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)        
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            addresse = form.cleaned_data['addresse']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
           
            wilaya_id = form['wilaya'].value()
            commune_id = form['commune'].value()
            note = form['note'].value()
            
            wilaya =  get_object_or_404(Wilaya, id=wilaya_id)
            commune = get_object_or_404(Commune, id=commune_id, wilaya=wilaya)
            try:
                order = Order.objects.create(first_name=first_name, last_name=last_name, addresse=addresse, phone=phone, email=email, wilaya=wilaya, commune=commune, note=note)   
                OrderItem.objects.create(order=order,product=product, price=product.price,quantity=1)         
            except:
                print('Some error occured')
                raise
            #order_created.delay(order.id)
            
            return render(request, 'order_created.html', {'order': order})
        else:
            return redirect(request, 'order.html', {'product_id': product_id})
    else:
        form = OrderCreateForm()
        
    wilayas = Wilaya.objects.all()
    return render(request, 'order.html', {'form' : form, 'wilayas': wilayas, 'product_id': product_id})


def load_communes_json(request):
    try:
        wilaya_id = request.GET.get('wilaya')
        wilaya = Wilaya.objects.filter(id=wilaya_id)
        
        communes = Commune.objects.filter(wilaya=wilaya_id)
        
        context = json.dumps(serializers.serialize('json', communes))
        
        return HttpResponse(context, content_type='application/json')
    except:
        return HttpResponse('', content_type='application/json')
   



def load_wilaya_json(request):
    try:
        wilaya_id = request.GET.get('wilaya')
        wilaya = Wilaya.objects.filter(id=wilaya_id)
        
        context = json.dumps(serializers.serialize('json', wilaya))
        return HttpResponse(context, content_type='application/json')
    except: 
        return HttpResponse('', content_type='application/json')
        