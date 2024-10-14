from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from . models import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

class ShowAllProfilesView(ListView):

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile']= profile
        return context
    
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        #attach the article to the new Comment
        # (forms.instance is the new comment objects)
        form.instance.profile = profile


        # delegate work to the superclass version of this method
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse("show_profile", kwargs=self.kwargs)