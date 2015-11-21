"""B512 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

import mymap.views

#RESTful API
from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', mymap.views.CustomerViewSet)
router.register(r'orders', mymap.views.OrderViewSet)
router.register(r'users', mymap.views.UserViewSet)


urlpatterns = [
	url(r'^$', mymap.views.customer, name='customer'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^calc/', mymap.views.calc,name='calc'),
	url(r'^order/', mymap.views.order,name='order'),
	url(r'^savecustomerform/', mymap.views.savecustomerform,name='savecustomerform'), #this is a ajax request
	url(r'^testing/', mymap.views.testing,name='testing'),
	url(r'^thanks/', mymap.views.thanks,name='thanks'),
	url(r'^about/', mymap.views.about,name='about'),
	url(r'^contact/', mymap.views.contact,name='contact'),
	url(r'^customer/', mymap.views.customer,name='customer'),
	url(r'^map/', mymap.views.map,name='map'),
	url(r'^show/', mymap.views.showcustomers,name='show'),
	url(r'^map/', mymap.views.home,name='map'),
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
]

urlpatterns += staticfiles_urlpatterns()