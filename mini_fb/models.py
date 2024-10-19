from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False, unique=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return messages
    
    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.id)])
    
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