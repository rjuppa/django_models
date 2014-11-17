
from django.forms import ModelForm
from django.forms.widgets import *
from bootstrap3_datetime.widgets import DateTimePicker
from coupons.models import Coupon


DISCOUNTS = (
    ('', '0% discount'),
    ('DISCOUNT_10_PERCENT', '10% discount'),
    ('DISCOUNT_20_PERCENT', '20% discount'),
    ('DISCOUNT_30_PERCENT', '30% discount'),
    ('DISCOUNT_40_PERCENT', '40% discount'),
    ('DISCOUNT_50_PERCENT', '50% discount'),
    ('DISCOUNT_60_PERCENT', '60% discount'),
    ('DISCOUNT_70_PERCENT', '70% discount'),
    ('DISCOUNT_80_PERCENT', '80% discount'),
    ('DISCOUNT_90_PERCENT', '90% discount'),
    ('DISCOUNT_100_PERCENT', '100% discount')
)

PRODUCTS = (
    ('', 'None'),
    ('a3c70ba9-886a-4c6f-874c-b63cd054f626', 'buy_03month'),
    ('a42ebad4-0b1c-4731-accf-a35e316718cd', 'buy_06month'),
    ('436e823d-69d8-4608-83f4-60f320a82e32', 'buy_12month'),
    ('9dc2a47c-0dc3-42af-9dda-54ca206a37a3', 'buy_01diamonds'),
    ('51ecd40f-2999-4313-aea7-1ba3277e7822', 'buy_05diamonds'),
    ('5f41d886-b696-42fb-a3a8-368f80f99767', 'buy_10diamonds'),
)


class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('code', 'method_name',
                  'limit_time', 'time_from', 'time_to',
                  'limit_email', 'email',
                  'limit_count', 'counter_max',
                  'limit_product', 'product')
        widgets = {'time_from': DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
                   'time_to': DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
                   'email': EmailInput(),
                   'method_name': Select(choices=DISCOUNTS),
                   'product': Select(choices=PRODUCTS),
                   }

        labels = {
            'code': 'Code',
            'method_name': 'Discount',
            'limit_time': 'Limited by time',
            'limit_email': 'Limited by email',
            'limit_count': 'Limited by count',
            'limit_product': 'Limited by product',
            'time_from': 'From',
            'time_to': 'To',
            'email': 'Email',
            'counter_max': 'Max',
            'product': 'Product',
        }



