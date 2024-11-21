from django import forms
from .models import WProfile, WaterLog
from django.contrib.auth.models import User

class SearchFriendForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Search username...'}),
        label=''
    )

class AddWaterLogForm(forms.ModelForm):
    class Meta:
        model = WaterLog
        fields = ['amount_consumed', 'water_type']

class CreatProfileForm(forms.ModelForm):
    class Meta:
        model = WProfile
        fields = ['user_name', 'profile_img', 'gender', 'DOB', 'Goal']