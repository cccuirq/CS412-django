from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False, unique=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'