django_models
=============

 Sample django model/form class implementation including validation.<br/>
 Sample uses python 3.<br/>

Installation:
============
  pip3 install django.<br/>
  pip3 install django-bootstrap3-datetimepicker.<br/>
  pip3 install pytz.<br/>

Run server: python manage.py runserver.<br/>

Navigate browser to: http://127.0.0.1:8000/coupons/newcoupon/.<br/>

Page newcoupon allows to create a discount coupon..<br/>
Coupon may have 4 limits:.<br/>
 1) time limit.<br/>
 2) count limit.<br/>
 3) email limit.<br/>
 4) product limit.<br/>
 5) any combination of above limits.<br/>


When it is submited, it's validated against restrictions defined in the model class..<br/>
When form is valid, it is saved to db or an error message is displayed..<br/>
Some basic tests are included.

