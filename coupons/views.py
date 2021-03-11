from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

"""
We get the current time to check if the coupon is valid, we search for one in the database
that meet the requirements, and if it does then we add the coupon id to the session then we
redirect the user to the cart_detail URL to display the cart with the coupon applied.
"""

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            #iexact : case insensitive exact match, lte: less than or equal, gte: greater than or equal, while exact is case sensitive
            coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            if(coupon.stock > 0 ):
                request.session['coupon_id'] = coupon.id
            else:
                print('Coupon non disponible')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
                
    return redirect('cart:cart_detail')