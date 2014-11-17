import string
import random
import datetime
from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.core.validators import *

class CouponManager(models.Manager):
    """
    Coupon manager class
    """

    @staticmethod
    def generate_code():
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(chars) for _ in range(6))
        return 'LANGEVO' + code

    def create_coupon(self):
        # create
        c = Coupon(code=self.generate_code(),
                   limit_time=True,
                   time_from=timezone.now().today(),
                   time_to=timezone.now().today() + datetime.timedelta(days=30),
                   limit_email=False,
                   email='',
                   limit_count=True,
                   counter=0,
                   counter_max=1,
                   limit_product=False,
                   product='',
                   data='',
                   status=0)
        return c


class Coupon(models.Model):
    """
    Coupon model
    """
    class Meta:
        db_table = 'lng_coupon'

    code = models.CharField(unique=True, db_index=True, max_length=20, blank=False, null=False,
                            validators=[RegexValidator(
                                        regex='^[A-Z0-9]*$',
                                        message='Code must be Alphanumeric',
                                        code='invalid_code'),
                                        ])
    method_name = models.CharField(max_length=50, blank=False, null=False)     # DISCOUNT_50_PERCENT
    limit_time = models.BooleanField(default=False)
    time_from = models.DateTimeField(null=True, blank=True)
    time_to = models.DateTimeField(null=True, blank=True)
    limit_email = models.BooleanField(default=False)
    email = models.CharField(max_length=50, blank=True, null=True)
    limit_count = models.BooleanField(default=False)
    counter = models.PositiveIntegerField(default=0)
    counter_max = models.PositiveIntegerField(default=0)
    limit_product = models.BooleanField(default=False)
    product = models.CharField(max_length=255, blank=True, null=True)
    data = models.CharField(max_length=255, blank=True, null=True)
    status = models.PositiveIntegerField(default=0)           # 0=new, 1=active not completed, 2=completed
    modified = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)

    objects = CouponManager()

    def clean(self):
        """
         Validates coupon
        """
        # Validation time
        if self.limit_time:
            if not self.time_from:
                raise ValidationError('time_from is required.')
            if not self.time_to:
                raise ValidationError('time_to is required.')
            if self.time_from >= self.time_to:
                raise ValidationError('time_to is earlier then time_from.')
        else:
            self.time_from = None
            self.time_to = None

        if self.time_from and not self.limit_time:
            raise ValidationError('time_from is set, but limit was not activated.')
        if self.time_to and not self.limit_time:
            raise ValidationError('time_to is set, but limit was not activated.')

        # Validation email
        if self.limit_email:
            if not self.email:
                raise ValidationError('email is required.')

            validate_email(self.email)

        if self.email and not self.limit_email:
            raise ValidationError('email is set, but limit was not activated.')

        # Validation count
        if self.limit_count:
            if self.counter_max < 1:
                raise ValidationError('counter_max must be positive integer.')
        else:
            self.counter_max = 0

        if self.counter_max > 0 and not self.limit_count:
            raise ValidationError('counter_max is set, but limit was not activated.')

        # Validation product
        if self.limit_product:
            if not self.product:
                raise ValidationError('product is required.')

        if self.product and not self.limit_product:
            raise ValidationError('product is set, but limit was not activated.')

        # Status
        if self.status<0 and self.status>=2:
            raise ValidationError('status is invalid.')

        # method_name
        if not self.method_name:
            raise ValidationError('method_name is required.')


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Coupon, self).save(*args, **kwargs)

    def activate(self):
        """
         Set coupon active means coupon is ready to use
        """
        if self.status == 2:
            raise ValueError(message='Coupon was already used.')

        self.status = 1
        self.full_clean()
        self.save()

    def apply_coupon(self, user, product_id):
        """
         Check limits
        """
        if self.status == 0:
            raise ValueError(message='Coupon is inactive.')

        if self.status == 2:
            raise ValueError(message='Coupon was already used.')

        if self.limit_time:
            if self.time_to < timezone.now():
                raise ValueError(message='Coupon has expired.')
            if self.time_from > timezone.now():
                raise ValueError(message='Coupon is applicable in future.')
        if self.limit_count:
            if self.counter >= self.counter_max:
                raise ValueError(message='Coupon was already used.')

        if self.limit_email:
            if self.email.lower() != user.email.lower():
                raise ValueError(message='You are not authorized to use this coupon.')

        if self.limit_product:
            if self.product.lower() != product_id.lower():
                raise ValueError(message='The coupon is not applicable to the product.')

        # NOT IMPLEMENTED
        if self.method_name == 'DO_SOMETHING':
            pass

        # ================
        # success coupon
        # ================
        self.status = 2                        # 2=completed

        if self.limit_count:
            self.counter += 1
            if self.counter < self.counter_max:
                self.status = 1                # 1=active not completed
        self.save()

        # write a log
        chist = CouponHistory(code=self.code, email=user.email, user_id=user.id)
        chist.full_clean()
        chist.save()
        return True

    def __str__(self):
        return smart_text('Coupon_'+str(self.code))


class CouponHistory(models.Model):
    """
    Just table for logging usage of coupons (no relations)
    """
    class Meta:
        db_table = 'lng_coupon_history'

    code = models.CharField(max_length=20, blank=False, null=False)
    user_id = models.PositiveIntegerField(default=0)
    email = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(CouponHistory, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text('Coupon_'+str(self.code))



