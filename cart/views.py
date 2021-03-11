from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm

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


"""
User can remove without problem, anyways the order is not validated yet
"""

@require_POST
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


def cart_detail(request):
    
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={ 'quantity': item['quantity']})

    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    }
    return render(request, 'cart_detail.html', context)