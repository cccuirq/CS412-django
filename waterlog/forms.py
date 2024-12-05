from django import forms
from .models import WProfile, WaterLog
from django.contrib.auth.models import User
from .models import Notification

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

class NotificationReadForm(forms.Form):
    notification_ids = forms.ModelMultipleChoiceField(
        queryset=Notification.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['notification_ids'].queryset = Notification.objects.filter(
                wprofile=user_profile,
                read=False
            )
