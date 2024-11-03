from django.db import models
from django.urls import reverse
import random
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False, unique=True)
    profile_image_url = models.URLField(blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return messages
    
    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.id)])
    
    def get_friends(self):
        friends1 = Friend.objects.filter(profile1 = self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2 = self).values_list('profile1', flat=True)

        friends = list(friends1) + list(friends2)
        freindsp = Profile.objects.filter(id__in=friends)
        return freindsp
    
    def add_friend(self, other):
        if self == other:
            raise ValueError("A profile cannot friend itself.")
        
        friendship_exists = Friend.objects.filter(models.Q(profile1 = self, profile2=other) | models.Q(profile1=other, profile2=self)).exists()
        if friendship_exists:
            print(f"Friendship between {self} and {other} already exists.")
            return
        
        new_friend = Friend(profile1=self, profile2 = other)
        new_friend.save()
        print(f"Friendship between {self} and {other} added successfully.")

    def get_friend_suggestions(self):
        all_profiles = Profile.objects.exclude(pk = self.pk)
        currentf = self.get_friends().values_list('pk', flat=True)
        nonf = all_profiles.exclude(pk__in=currentf)
        non_friends_list = list(nonf)
        random.shuffle(non_friends_list)
        return non_friends_list[:3]
    
    def get_news_feed(self):
        own_message = StatusMessage.objects.filter(profile=self)

        friends = self.get_friends()
        friends_message = StatusMessage.objects.filter(profile__in=friends)
        all_mess = (own_message | friends_message).order_by('-timestamp')

        return all_mess
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile =  models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.message}'
    
    def get_images(self):
        images = Image.objects.filter(status_message = self)
        return images

class Image(models.Model):
    image_file = models.ImageField(blank=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.status_message}'

class Friend(models.Model):
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1} & {self.profile2}'
    
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()