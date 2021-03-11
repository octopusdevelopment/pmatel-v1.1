from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse


from django.conf import settings
from django.core import serializers
from django.template.loader import render_to_string
import weasyprint
import json

from .models import OrderItem, Wilaya, Commune, Order
from main.models import Product
from cart.cart import Cart
from coupons.models import Coupon
from .forms import OrderCreateForm, OrderProductQuantityForm
from coupons.forms import CouponApplyForm
from .tasks import order_created
from django.utils import timezone
from decimal import Decimal


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    wilayas = Wilaya.objects.all()
    
    if request.method == 'POST':
        if len(cart):
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                if cart.coupon:
                    coupon = Coupon.objects.get(id = cart.coupon.id, stock__gt=0)
                    if coupon: 
                        order.coupon = cart.coupon
                        order.discount_amount = cart.get_discount()
                        coupon.stock = coupon.stock - 1
                        coupon.save()
                order.save()
                products_total = []
                for item in cart:
                    product_price = item['price'] * item ['quantity']
                    products_total.append(product_price)
                    
                    OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                
                # Get total price to display
                total_price = cart.get_total_price_after_discount()
                
                cart.clear()
                order_created.delay(order.id)
                
                context = {'order': order,
                           'products_total': products_total, 
                           'total_price': total_price,
                           }
                return render(request, 'order_created.html', context)
        else:
            return redirect(request, 'catalog.html')
    else:
        form = OrderCreateForm()
    
    return render(request, 'order.html', {'cart':cart, 'form' : form, 'wilayas': wilayas})



def order_create_one_product(request, product_id):
    
    #add later: quantity > X
    product = get_object_or_404(Product, id=product_id)        
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        quantity_form = OrderProductQuantityForm(request.POST)
        if form.is_valid() & quantity_form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            addresse = form.cleaned_data['addresse']
            phone = form.cleaned_data['phone']
            quantity = quantity_form.cleaned_data['quantity']
            email = form.cleaned_data['email']
           
            wilaya_id = form['wilaya'].value()
            commune_id = form['commune'].value()
            note = form['note'].value()
            
            wilaya =  get_object_or_404(Wilaya, id=wilaya_id)
            commune = get_object_or_404(Commune, id=commune_id, wilaya=wilaya)
            
            # check if the coupon code is valid, it's not important if it is not, worst case user won't get a discount
            now = timezone.now()
            coupon_form = CouponApplyForm(request.POST)
            if coupon_form.is_valid():
                code = coupon_form.cleaned_data['code']
                try:
                    #lte: less than or equal, gte: greater than or equal, while exact is case sensitive
                    coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True, stock__gte=1)
                    discount = get_discount(product, coupon)
                    total_price = product.price - discount
                    
                except Coupon.DoesNotExist:
                    coupon = None
                    total_price = product
                    discount = 0
            else:
                coupon = None
                total_price = product
                discount = 0
            try:
                order = Order.objects.create(first_name=first_name, last_name=last_name, addresse=addresse, phone=phone, email=email, wilaya=wilaya, commune=commune, note=note, coupon=coupon, discount_amount = discount)   
                OrderItem.objects.create(order=order,product=product, price=product.price,quantity=quantity)
                # reduce quantity
                if coupon:
                    coupon.stock = coupon.stock - 1
                    coupon.save()
                    
                order_created.delay(order.id)        
            except:
                print('Some error occured')
                raise
            
            context = {'order': order,
                           'products_total': total_price, 
                           'total_price': total_price,
                      }
            return render(request, 'order_created.html', context)
        else:
            form = OrderCreateForm()
            coupon_form = CouponApplyForm()
            return redirect(request, 'order.html', {'product_id': product_id, 'form': form, 'coupon_form': coupon_form})
    else:
        form = OrderCreateForm()
        coupon_form = CouponApplyForm()
        
    wilayas = Wilaya.objects.all()
    return render(request, 'order.html', {'form' : form, 'wilayas': wilayas, 'product_id': product_id, 'show_quantity_field': True, 'coupon_form': coupon_form})


# Show order details
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'admin/orders/order/detail.html', {'order': order})


# Display order details as pdf
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('admin/orders/order/pdf.html', {'order': order})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    weasyprint.HTML(string=html).write_pdf(response)
    return response


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


"""
This method is used when the user purchases directly a product       
"""     
def get_discount(product, coupon):
    if coupon:
            if coupon.discount_amount:
                return coupon.discount_amount
            else:
                return coupon.discount_percentage / Decimal(100) \
                * product.price
                
    return Decimal(0)
    
    