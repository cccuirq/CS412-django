from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
class WProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user_name = models.TextField(blank=False)
    profile_img = models.ImageField(blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    DOB = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    Goal = models.IntegerField()
    waterUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_profiles')
    def __str__ (self):
        return f'{self.user_name}'
    
    def get_water_log(self):
        return WaterLog.objects.filter(wprofile = self).order_by('timestamp')
    
    def get_friends(self):
        friends1 = friend.objects.filter(wprofile1 = self).values_list('wprofile2', flat=True)
        friends2 = friend.objects.filter(wprofile2 = self).values_list('wprofile1', flat=True)

        friends = list(friends1) + list(friends2)
        freindsp = WProfile.objects.filter(id__in=friends)
        return freindsp


class WaterLog(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    wprofile =  models.ForeignKey("WProfile", on_delete=models.CASCADE)
    amount_consumed = models.FloatField()
    water_type = models.CharField(max_length=50, choices=[('Cup', 'Cup'), ('Bottle', 'Bottle'), ('Can', 'Can'), ('L', 'L'), ('ml', 'ml')], default='Plain')

    def __str__(self):
        return f"{self.wprofile.user_name} - {self.amount_consumed} {self.water_type}"

class friend(models.Model):
    wprofile1 = models.ForeignKey("WProfile", on_delete=models.CASCADE, related_name="wprofile1")
    wprofile2 = models.ForeignKey("WProfile", on_delete=models.CASCADE, related_name="wprofile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.wprofile1} & {self.wprofile2}'
    
class Notification(models.Model):
    wprofile = models.ForeignKey("WProfile", on_delete=models.CASCADE)
    sender = models.ForeignKey("WProfile", on_delete=models.CASCADE, related_name="sent_notifications", null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.wprofile.user_name} from {self.sender.user_name if self.sender else 'Unknown'}: {self.message}"