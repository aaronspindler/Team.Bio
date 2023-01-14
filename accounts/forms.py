from django import forms

from accounts.models import User
from companies.models import Location, Team


class UserProfileForm(forms.ModelForm):
    short_bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": "3"}))
    profile_picture = forms.ImageField(label='')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['general_location'].queryset = Location.objects.filter(company=company)
        self.fields['general_location'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm'})

        self.fields['team'].queryset = Team.objects.filter(company=company)
        self.fields['team'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm'})

        self.fields['title'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm'})

        self.fields['short_bio'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'})

        self.fields['linkedin'].widget.attrs.update({'class': 'block w-full min-w-0 flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'})

        self.fields['twitter'].widget.attrs.update({'class': 'block w-full min-w-0 flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'})

        self.fields['github'].widget.attrs.update({'class': 'block w-full min-w-0 flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'})

        self.fields['first_name'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm'})

        self.fields['last_name'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm'})

        self.fields['address_1'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm', 'autocomplete': 'street-address'})
        self.fields['city'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm', 'autocomplete': 'city'})
        self.fields['prov_state'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm', 'autocomplete': 'state'})
        self.fields['postal_code'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm', 'autocomplete': 'country'})
        self.fields['country'].widget.attrs.update({'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:max-w-xs sm:text-sm', 'autocomplete': 'postal-code'})

        self.fields['profile_picture'].widget.attrs.update({'class': 'ml-5 rounded-md border border-gray-300 bg-white py-2 px-3 text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2'})

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
            'linkedin',
            'twitter',
            'github',
            'address_1',
            'city',
            'prov_state',
            'postal_code',
            'country',
        ]
