from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartAddProductQuantityForm
from coupons.forms import CouponApplyForm
# pagination
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
#json
from django.core import serializers
import json


"""
Verify if quantity is available, but we won't substract if from the stock unless the user purchases
"""
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    # Get the product that we want to add
    product = get_object_or_404(Product, id= product_id, available=True, stock__gte=1)
    product_slug = product.slug
    # Create a form using the data entered in the form
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        desired_quantity = cleaned_data['quantity']
        if product.stock > desired_quantity:
            quantity = desired_quantity
        elif product.stock < desired_quantity & product.stock > 10:
            quantity = 5
        else:
            quantity = 1
        print(f'User can take {quantity} of product {product.name}')
        cart.add(
            product=product,
            quantity=quantity,
        )
        return redirect('cart:cart_detail')
    else:
        return redirect(f'/produits/{product_slug}')


def cart_add_one_product(request, product_id):
    cart = Cart(request)
    # Get the product that we want to add
    product = get_object_or_404(Product, id= product_id, available=True, stock__gte=1)
    
    if product.stock >= 1:
            quantity = 1
    cart.add_one(
            product=product,
            quantity=quantity,
    )
    return redirect('/produits')


@require_POST
def cart_add_one_product_with_quantity(request, slug, product_id):
    cart = Cart(request)
    # Get the product that we want to add
    product = get_object_or_404(Product, id= product_id, available=True, stock__gte=1)
    
    form = CartAddProductQuantityForm(request.POST)
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        desired_quantity = cleaned_data['quantity']
        print(desired_quantity)
        if product.stock > desired_quantity:
            quantity = desired_quantity
        elif product.stock < desired_quantity & product.stock > 10:
            quantity = 5
        else:
            quantity = 1
        print(f'User can take {quantity} of product {product.name}')
        cart.add(
            product=product,
            quantity=quantity,
        )
        return redirect('cart:cart_detail')
    else:
        return redirect(f'/produits/{product.slug}', {'failed':True})

"""
User can remove without problem, anyways the order is not validated yet
"""


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    desired_quantity = int(request.POST.get('quantity'))
    if product.stock > desired_quantity:
        quantity = desired_quantity
    elif product.stock < desired_quantity & product.stock > 10:
        quantity = 5
    else:
        quantity = 1

    cart.update(product=product, quantity=quantity)
    return redirect('cart:cart_detail')



@require_POST
def cart_update_with_json(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    data = json.loads(request.body.decode("utf-8"))
    
    desired_quantity = int(data['quantity'])
    if product.stock > desired_quantity:
        quantity = desired_quantity
    elif product.stock < desired_quantity & product.stock > 10:
        quantity = 5
    else:
        quantity = 1

    cart.update(product=product, quantity=quantity)
    
    print("CART ITEM MODIFIED")
    res = {
        "name": product.name,
        "price": product.price,
        "quantity": quantity,
        "total-product": product.price * quantity,
        "sub-total": cart.get_total_price(),
        "total": cart.get_total_price_after_discount(),
        "number-products": cart.__len__()
    }
    return JsonResponse(res)

@require_POST

def cart_empty(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')
    

def cart_detail(request):
    
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    
    products = []
    items = []
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={ 'quantity': item['quantity']})
        item['total'] = item['product'].price * item['quantity']
        items.append(item)
        products.append(item['product'])
    page = request.GET.get('page')
    paginator = Paginator(items, 1000)
    
    try:
        list_products = paginator.get_page(page)
        
    except PageNotAnInteger:
        list_products = paginator.get_page(1)
        
    except EmptyPage:
        list_products = paginator.get_page(paginator.num_pages)
    
    context = {
        'cart': cart,
        'listing_products': list_products,
        'coupon_apply_form': coupon_apply_form
    }
    return render(request, 'cart/cart-page.html', context)



        
        
    