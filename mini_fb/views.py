from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from . models import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
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
        
        sm = form.save()
        files = self.request.FILES.getlist('files')
        print(f"Files uploaded: {files}")

        for file in files:
            image = Image()
            image.image_file = file
            image.status_message = sm
            image.save()

            print(f"Saved image for status message: {sm} with file: {file}")

        # delegate work to the superclass version of this method
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse("show_profile", kwargs=self.kwargs)
    
class UpdateProfileView(UpdateView):
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile

class DeleteStatusMessageView(DeleteView):
    template_name = 'mini_fb/delete_status_form.html'
    model = StatusMessage
    context_object_name = 'message'
    
    def get_success_url(self) -> str:
        pk = self.kwargs.get('pk')
        status = StatusMessage.objects.filter(pk=pk).first()

        profile = status.profile
        return reverse("show_profile", kwargs={'pk':profile.pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    form_class = UpdateStatusMessageForm 
    context_object_name = 'Umessage'

    def form_valid(self, form):
        # Save the updated status message
        sm = form.save()

        files = self.request.FILES.getlist('files') 
        for file in files:
            image = Image()
            image.image_file = file
            image.status_message = sm
            image.save()

        return super().form_valid(form)
    

    def get_success_url(self) -> str:
        status = self.get_object()
        return reverse('show_profile', kwargs={'pk': status.profile.pk})
    
class DeleteImageView(DeleteView):
    model = Image
    template_name = 'mini_fb/delete_image_form.html'
    context_object_name = 'image'

    def get_success_url(self):
        image = self.get_object()
        return reverse('update_status', kwargs={'pk': image.status_message.pk})
