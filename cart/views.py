from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    # Get the product that we want to add
    product = get_object_or_404(Product, id= product_id)
    product_slug = product.slug
    # Create a form using the data entered in the form
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(
            product=product,
            quantity=cleaned_data['quantity'],
        )
        return redirect('cart:cart_detail')
    else:
        return redirect(f'/produits/{product_slug}')



@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={ 'quantity': item['quantity']})

    context = {
        'cart': cart,
    }
    return render(request, 'cart_detail.html', context)



@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity'))
    print('Quantity', quantity)
    cart.update(product=product, quantity=quantity)
    return redirect('cart:cart_detail')