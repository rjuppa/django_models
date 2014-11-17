from django.conf.urls import patterns, url
from coupons.views import *


urlpatterns = patterns('',
    # ex: /language/
    # url(r'^$', index),

    url(r'^newcoupon/$', new_coupon_page),

)
