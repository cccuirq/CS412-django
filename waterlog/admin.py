from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(WProfile)
admin.site.register(WaterLog)
admin.site.register(friend)
admin.site.register(Notification)