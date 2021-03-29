from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse


from django.core import serializers
from django.template.loader import render_to_string
import weasyprint
import json

from .models import OrderItem, Wilaya, Commune, Order
from .utils import manage_quantity, get_discount
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
                order.delivery = order.wilaya.price
                now = timezone.now()
                if cart.coupon:
                    coupon = Coupon.objects.get(id=cart.coupon.id, valid_from__lte=now, valid_to__gte=now, active=True, stock__gte=1)
                    if coupon:
                        order.coupon = cart.coupon
                        order.discount_amount = cart.get_discount()
                        coupon.stock = coupon.stock - 1
                        coupon.save()
                        print('HERE ONE!!!')
                order.save()
                products_total = []
                for item in cart:
                    product_price = item['price'] * item ['quantity']
                    products_total.append(product_price)

                    OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                print('ORDER ITEM CREATED')
                # Get total price to display
                total_price = cart.get_total_price_after_discount() + order.wilaya.price

                cart.clear()
                order_created(order)

                context = {'order': order,
                           'products_total': products_total,
                           'total_price': total_price,
                           }
                return render(request, 'order/order-created.html', context)
        else:
            return redirect(request, 'catalog.html')
    else:
        form = OrderCreateForm()

    return render(request, 'order/checkout.html', {'cart':cart, 'form' : form, 'wilayas': wilayas})

def order_create_one_product(request, product_id):

    #add later: quantity > X
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        order = None
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
                    total_price = product.price + wilaya.price
                    discount = 0
            else:
                coupon = None
                total_price = product.price + wilaya.price
                discount = 0
            try:
                can_be_ordered = manage_quantity(product, quantity)
                print(can_be_ordered)
                if can_be_ordered["success"] == True:

                    quantity = can_be_ordered["quantity"]
                    order = Order.objects.create(first_name=first_name, last_name=last_name, addresse=addresse, phone=phone, email=email, wilaya=wilaya, commune=commune, note=note, coupon=coupon, discount_amount = discount, delivery=wilaya.price)
                    OrderItem.objects.create(order=order,product=product, price=product.price,quantity=quantity)
                    # reduce quantity
                    if coupon:
                        coupon.stock = coupon.stock - 1
                        coupon.save()
                    order_created(order)
                    context = {'order': order,
                           'products_total': total_price,
                           'total_price': total_price,
                      }
                    return render(request, 'order/order-created.html', context)
                else:
                    print('cannot be ordered')
                    #return render(request, 'order/order-created.html', context)
                #order_created.delay(order.id)
            except:
                print('Some error occured')
                raise

        else:

            form = OrderCreateForm()
            coupon_form = CouponApplyForm()
            return redirect(request, 'order/checkout.html', {'product_id': product_id, 'product': product, 'form': form, 'coupon_form': coupon_form})
    else:
        form = OrderCreateForm()
        coupon_form = CouponApplyForm()

    wilayas = Wilaya.objects.filter(active=True)
    return render(request, 'order/checkout.html', {'form' : form, 'wilayas': wilayas, 'product': product, 'product_id': product_id, 'show_quantity_field': True, 'coupon_form': coupon_form})


def load_communes_json(request):
    try:
        wilaya_id = request.GET.get('wilaya')

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

@require_POST
def order_update_quantity(request):
    data = json.loads(request.body.decode("utf-8"))
    desired_quantity = int(data['quantity'])
    product_id = data['product_id']
    discount = Decimal(data['discount'])

    product = get_object_or_404(Product, id=product_id, available=True)
    print(product.name)
    try:
        if product.stock > 0:
            if product.stock > desired_quantity:
                quantity = desired_quantity
            elif product.stock < desired_quantity & product.stock > 10:
                quantity = 5
            else:
                quantity = 1

            total = product.price * quantity

            res = {
                "success": True,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "total-product": total,
                "total": total - total * discount,
            }
            print('response: -------------------', res)
        else:
            res = {
            'success': False,}
    except:
        res = {
            'success': False
        }
    return JsonResponse(res)

@require_POST
def order_apply_coupon(request):
    data = json.loads(request.body.decode("utf-8"))
    code = data['coupon_code']
    now = timezone.now()
    try:
        coupon = get_object_or_404(Coupon, code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True, stock__gte=1)
        if coupon:
            res = {
                "success": True,
                "code": coupon.code,
                "amount": coupon.discount_amount,
                "percentage": coupon.discount_percentage
                }

        else:
            res = {'success': False}
    except:
        res = {'success': False}
    return JsonResponse(res)


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
    #weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    weasyprint.HTML(string=html).write_pdf(response)
    return response
