from django.test import TestCase

from django.test import TestCase
from coupons.models import Coupon
from django.contrib.auth.models import User

class CouponTestCase(TestCase):
    def setUp(self):
        # coupon 20% discount
        c = Coupon.objects.create_coupon()
        c.code = 'LANGEVOCBVZM2'
        c.method_name = 'DISCOUNT_20_PERCENT'
        c.limit_product = True
        c.product = 'a3c70ba9-886a-4c6f-874c-b63cd054f626'
        c.save()

        # coupon 50% discount
        c = Coupon.objects.create_coupon()
        c.code = 'LANGEVOPZT737'
        c.method_name = 'DISCOUNT_50_PERCENT'
        c.limit_product = True
        c.product = 'a3c70ba9-886a-4c6f-874c-b63cd054f626'
        c.limit_email = True
        c.email = 'rjuppa@gmail.com'
        c.save()

        c = Coupon.objects.create_coupon()
        c.code = 'LANGEVO0RHP6D'
        c.method_name = 'DISCOUNT_10_PERCENT'
        c.limit_product = True
        c.product = 'a3c70ba9-886a-4c6f-874c-b63cd054f626'
        c.limit_count = True
        c.counter_max = 3
        c.save()

        u = User.objects.create_user('admin', 'rjuppa@gmail.com', 'password')


    def test_coupon_20percent_1month(self):
        """ Coupon 20% has correct method name, limit_time and status """
        c = Coupon.objects.get(code='LANGEVOCBVZM2')
        self.assertEqual(c.method_name, 'DISCOUNT_20_PERCENT')
        self.assertTrue(c.limit_time)
        self.assertEqual(c.status, 0)

    def test_coupon_50percent_with_email_1month(self):
        """ Coupon 50% has correct method name , limit_time, status and email """
        c = Coupon.objects.get(code='LANGEVOPZT737')
        self.assertEqual(c.method_name, 'DISCOUNT_50_PERCENT')
        self.assertTrue(c.limit_time)
        self.assertTrue(c.limit_email)
        self.assertEqual(c.email, 'rjuppa@gmail.com')
        self.assertEqual(c.status, 0)

    def test_coupon_10percent_for_3people_1month(self):
        """ Coupon 10% has correct method name, limit_time, count_limit and status """
        c = Coupon.objects.get(code='LANGEVO0RHP6D')
        self.assertEqual(c.method_name, 'DISCOUNT_10_PERCENT')
        self.assertTrue(c.limit_time)
        self.assertTrue(c.limit_count)
        self.assertEqual(c.counter_max, 3)
        self.assertEqual(c.counter, 0)
        self.assertEqual(c.status, 0)

    def test_activate_coupon_20percent(self):
        """ Active coupon 20% has correct status """
        c = Coupon.objects.get(code='LANGEVOCBVZM2')
        self.assertEqual(c.status, 0)
        c.activate()
        self.assertEqual(c.status, 1)

    def test_apply_coupon_20percent(self):
        """ Apply coupon 20% has correct status """
        c = Coupon.objects.get(code='LANGEVOCBVZM2')
        self.assertEqual(c.status, 0)

        c.activate()
        self.assertEqual(c.status, 1)

        user = User.objects.get(pk=1)
        c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')
        self.assertEqual(c.status, 2)

    def test_apply_coupon_twice_raise_error(self):
        """ Active coupon twice raise error """
        c = Coupon.objects.get(code='LANGEVOCBVZM2')
        c.activate()
        user = User.objects.get(pk=1)
        c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')
        self.assertEqual(c.status, 2)
        #  raise ValueError when called second time
        with self.assertRaises(ValueError):
            c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')

    def test_apply_coupon_with_wrong_product_raise_error(self):
        """ Active coupon with wrong product raise error """
        c = Coupon.objects.get(code='LANGEVOPZT737')
        c.activate()
        user = User.objects.get(pk=1)
        with self.assertRaises(ValueError):
            c.apply_coupon(user=user, product_id='a3c70ba9-1111-2222-3333-b63cd054f626')

    def test_apply_coupon_with_correct_person(self):
        """ Active coupon by correct person raise error """
        c = Coupon.objects.get(code='LANGEVOPZT737')
        c.activate()
        user = User.objects.get(pk=1)
        c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')
        self.assertEqual(c.status, 2)


    def test_apply_coupon_with_wrong_person_raise_error(self):
        """ Active coupon by wrong person raise error """
        c = Coupon.objects.get(code='LANGEVOPZT737')
        c.activate()

        user = User.objects.create_user('wrong', 'wrong@gmail.com', 'wrong')
        #  raise ValueError when called second time
        with self.assertRaises(ValueError):
            c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')


    def test_apply_coupon_more_then_count_max_raise_error(self):
        """ Active coupon more then count limit raise error """
        c = Coupon.objects.get(code='LANGEVO0RHP6D')
        c.activate()
        user = User.objects.get(pk=1)
        c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')
        c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')
        c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')
        with self.assertRaises(ValueError):
            c.apply_coupon(user=user, product_id='a3c70ba9-886a-4c6f-874c-b63cd054f626')