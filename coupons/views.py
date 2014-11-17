import datetime
from django.shortcuts import render
from coupons.models import Coupon
from coupons.forms import CouponForm


def new_coupon_page(request):

    if request.method == 'POST':
        # POST
        form = CouponForm(request.POST)

        if form.is_valid():
            # save to DB
            form.save()
            return render(request, 'coupons/coupon_created.html', { 'form': form, })
    else:
        # GET
        # display coupon
        new_coupon = Coupon.objects.create_coupon()
        form = CouponForm(instance=new_coupon)

    return render(request, 'coupons/new_coupon.html', { 'form': form, })



