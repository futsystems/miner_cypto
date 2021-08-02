# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from gamefi import views

urlpatterns = [
    url(r'^index$', views.homepage, name='index'),
]