django_models
=============

 Sample django model/form class implementation including validation.
 Sample uses python 3

Installation:
============
  pip3 install django
  pip3 install django-bootstrap3-datetimepicker
  pip3 install pytz

Run server: python manage.py runserver

Navigate browser to: http://127.0.0.1:8000/coupons/newcoupon/

Page newcoupon allows to create a discount coupon.
Coupon may have 4 limits:
 1) time limit
 2) count limit
 3) email limit
 4) product limit
 5) any combination of above limits


When it is submited, it's validated against restrictions defined in the model class.
When form is valid, it is saved to db or an error message is displayed.
Some basic tests are included.

