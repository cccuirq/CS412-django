# ma/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResultsListView.as_view(), name="home"),
    path(r'results', views.ResultsListView.as_view(), name="results"),
    path(r'results/<int:pk>', views.ResultDetailView.as_view(), name="results_detail"),
]