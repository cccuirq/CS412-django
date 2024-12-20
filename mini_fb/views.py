from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from . models import *
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import Http404

class ShowAllProfilesView(ListView):

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk:
            # If a pk is provided, retrieve the specific profile
            return get_object_or_404(Profile, pk=pk)
        else:
            # If no pk is provided, retrieve the logged-in user's profile
            user_profiles = Profile.objects.filter(user=self.request.user)
            return user_profiles.order_by('?').first()

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            # If not authenticated, handle user creation
            user_creation_form = UserCreationForm(self.request.POST)
            
            if user_creation_form.is_valid():
                # Save the new user and get the User instance
                user = user_creation_form.save()
                # Attach the new user to the Profile instance
                form.instance.user = user
                # Log the user in automatically after registration
                login(self.request, user)
                print("New user and profile successfully created.")
            else:
                # If UserCreationForm is invalid, re-render the form with errors
                print("UserCreationForm errors:", user_creation_form.errors)
                return self.form_invalid(form)
        else:
            # For authenticated users, attach the new profile to the current user
            form.instance.user = self.request.user
            print("Profile successfully created for existing user.")

        # Proceed with saving the profile
        return super().form_valid(form)

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Retrieve profile_id from query parameters
        profile_id = self.request.GET.get('profile_id')
        
        # Ensure profile_id is provided
        if profile_id:
            profile = get_object_or_404(Profile, user=self.request.user, id=profile_id)
            context['profile'] = profile
        else:
            raise Http404("Profile ID not provided or invalid")
        
        return context
    
    def form_valid(self, form):
         # Retrieve profile_id from query parameters
        profile_id = self.request.GET.get('profile_id')
        
        # Ensure profile_id is provided
        if profile_id:
            profile = get_object_or_404(Profile, user=self.request.user, id=profile_id)
            form.instance.profile = profile
        else:
            raise Http404("Profile ID not provided or invalid")
        
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
        profile_id = self.request.GET.get('profile_id')
        return reverse("show_profile", kwargs={'pk': profile_id})
    
    def get_login_url(self) -> str:

        return reverse('login')
    
    def get_object(self):
        profile_id = self.request.GET.get('profile_id')
        
        # Debugging output
        print("Profile ID from query parameters:", profile_id)
        
        if profile_id:
            profile = get_object_or_404(Profile, user=self.request.user, id=profile_id)
            print("Profile found:", profile)
            return profile
        else:
            raise Http404("Profile ID not provided or invalid")
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile

    def get_object(self):
        profile_id = self.request.GET.get('profile_id')
        
        # Debugging output
        print("Profile ID from query parameters:", profile_id)
        
        if profile_id:
            profile = get_object_or_404(Profile, user=self.request.user, id=profile_id)
            print("Profile found:", profile)
            return profile
        else:
            raise Http404("Profile ID not provided or invalid")

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    template_name = 'mini_fb/delete_status_form.html'
    model = StatusMessage
    context_object_name = 'message'
    
    def get_success_url(self) -> str:
        pk = self.kwargs.get('pk')
        status = StatusMessage.objects.filter(pk=pk).first()

        profile = status.profile
        return reverse("show_profile", kwargs={'pk':profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
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

    
class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'mini_fb/delete_image_form.html'
    context_object_name = 'image'

    def get_success_url(self):
        image = self.get_object()
        return reverse('update_status', kwargs={'pk': image.status_message.pk})

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        profile_id = request.GET.get('profile_id')
        
        if profile_id:
            user_profile = get_object_or_404(Profile, user=request.user, id=profile_id)
        else:
            raise Http404("Profile ID not provided or invalid")

        friend_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        
        user_profile.add_friend(friend_profile)
        
        return redirect(reverse('show_profile', kwargs={'pk': user_profile.pk}))
    
    def get_object(self):
        profile_id = self.request.GET.get('profile_id')
        
        # Debugging output
        print("Profile ID from query parameters:", profile_id)
        
        if profile_id:
            profile = get_object_or_404(Profile, user=self.request.user, id=profile_id)
            print("Profile found:", profile)
            return profile
        else:
            raise Http404("Profile ID not provided or invalid")
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    template_name = 'mini_fb/friend_suggestions.html'
    model = Profile
    context_object_name = "suggestion"

    def get_object(self):
        profile_id = self.request.GET.get('profile_id')
        
        # Debugging output
        print("Profile ID from query parameters:", profile_id)
        
        if profile_id:
            profile = get_object_or_404(Profile, user=self.request.user, id=profile_id)
            print("Profile found:", profile)
            return profile
        else:
            raise Http404("Profile ID not provided or invalid")

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    template_name = 'mini_fb/news_feed.html'
    model = Profile
    context_object_name = "newsFeed"

    def get_object(self):
        profile_id = self.request.GET.get('profile_id')
        
        # Debugging output
        print("Profile ID from query parameters:", profile_id)
        
        if profile_id:
            profile = get_object_or_404(Profile, user=self.request.user, id=profile_id)
            print("Profile found:", profile)
            return profile
        else:
            raise Http404("Profile ID not provided or invalid")
        
