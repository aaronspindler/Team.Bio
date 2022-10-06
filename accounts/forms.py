from django import forms
from django.forms import ModelForm

from accounts.models import CustomUser


class UserProfileForm(ModelForm):
    profile_picture = forms.ImageField(label="Profile Picture")
    short_bio = forms.CharField(
        label="Bio",
        widget=forms.TextInput(
            attrs={'placeholder': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'}
        )
    )
    title = forms.CharField(
        label="Job Title",
        widget=forms.TextInput(
            attrs={'placeholder': 'Chief Fun Officer'}
        )
    )

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'short_bio', 'title']
