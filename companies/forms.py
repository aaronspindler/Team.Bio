from django import forms
from django.forms import ModelForm

from companies.models import Company, Location


class CompanyForm(ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Magma Health'}))
    url = forms.CharField(label="URL", widget=forms.TextInput(attrs={'placeholder': 'https://www.magmahealth.com'}))

    class Meta:
        model = Company
        fields = ['name', 'url']


class LocationForm(ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'NYC'}))

    class Meta:
        model = Location
        fields = ['name']
