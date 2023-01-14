from django import forms

from accounts.models import User
from companies.models import Location, Team


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    short_bio = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['general_location'].queryset = Location.objects.filter(company=company)
        self.fields['team'].queryset = Team.objects.filter(company=company)

    class Meta:
        model = User
        fields = [
            'profile_picture',
            'short_bio',
            'first_name',
            'last_name',
            'title',
            'general_location',
            'team',
            'linkedin_url',
            'twitter_url',
            'github_url',
            'address_1',
            'city',
            'prov_state',
            'postal_code',
            'country',
        ]
