from django import forms

from accounts.models import User


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="Profile Picture", required=False)
    short_bio = forms.CharField(
        label="Bio",
        widget=forms.Textarea(
            attrs={'placeholder': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'}
        ),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'profile_picture',
            'short_bio',
        ]
