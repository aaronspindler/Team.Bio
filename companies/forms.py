from django import forms
from django.forms import ModelForm

from companies.models import Company, Invite, Link, Location, Team


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


class CompanyFeatureForm(ModelForm):
    map_enabled = forms.BooleanField(
        label="Enabled / Disable the display of your company map on the company home page",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600",
            }
        ),
    )

    links_enabled = forms.BooleanField(
        label="Enabled / Disable the display of links on your company home page",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600",
            }
        ),
    )

    class Meta:
        model = Company
        fields = ["map_enabled", "links_enabled"]


class InviteForm(ModelForm):
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "placeholder": "fred@flintstones.com",
                "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
        ),
    )

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


class LinkForm(ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "PTO Policy",
                "class": "block w-full border-0 p-0 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6",
            }
        ),
    )
    url = forms.CharField(
        label="URL",
        widget=forms.TextInput(
            attrs={
                "placeholder": "https://www.magmahealth.com/pto-policy",
                "class": "block w-full border-0 p-0 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6",
            }
        ),
    )

    class Meta:
        model = Link
        fields = ["name", "url"]
