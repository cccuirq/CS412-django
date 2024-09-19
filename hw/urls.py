## hw/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

#create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name)
    path(r'', views.home, name = "home"), ##our first URL
    path(r'about', views.about, name = "about"), ##our first URL
]