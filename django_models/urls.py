from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_models.views.home', name='home'),
    url(r'^coupons/', include('coupons.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
