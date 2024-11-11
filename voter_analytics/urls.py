from django.urls import path
from . import views

urlpatterns = [
    path('', views.VotesListView.as_view(), name="home"),
    path('votes', views.VotesListView.as_view(), name="votes"),
    path(r'voter/<int:pk>', views.VotesDetailView.as_view(), name="votes_detail"),
    path(r'graphs', views.GraphsListView.as_view(), name="graphs"),
]