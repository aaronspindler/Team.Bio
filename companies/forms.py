from django import forms
from django.forms import ModelForm

from companies.models import Company, Invite, Location, Team


class CompanyForm(ModelForm):
    name = forms.CharField(
        label="Name", widget=forms.TextInput(attrs={"placeholder": "Magma Health"})
    )
    url = forms.CharField(
        label="URL",
        widget=forms.TextInput(attrs={"placeholder": "https://www.magmahealth.com"}),
    )

    class Meta:
        model = Company
        fields = ["name", "url"]


class InviteForm(ModelForm):
    class Meta:
        model = Invite
        fields = ["email"]


class LocationForm(ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "NYC",
                "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
        ),
    )

    class Meta:
        model = Location
        fields = ["name"]


class TeamForm(ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Engineering",
                "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
        ),
    )

    class Meta:
        model = Team
        fields = ["name"]
