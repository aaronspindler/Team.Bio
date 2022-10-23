from django import forms
from django.forms import ModelForm

from companies.models import Company, Location, Team


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


class TeamForm(ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Engineering'}))

    class Meta:
        model = Team
        fields = ['name']
