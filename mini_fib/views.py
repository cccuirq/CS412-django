from django.shortcuts import render

# Create your views here.
from . models import *
from django.views.generic import ListView

class ShowAllProfilesView(ListView):

    model = Profile
    template_name = "mini_fib/show_all_profiles.html"
    context_object_name = 'profiles'