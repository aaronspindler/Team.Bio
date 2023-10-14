from colorfield.fields import ColorField
from django import forms
from django.forms import ModelForm

from companies.models import BulkInviteRequest, Company, Invite, Link, Location, Team
from utils.constants import FILE_FIELD_CLASS


class CompanyForm(ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={"placeholder": "Magma Health"}))
    url = forms.CharField(
        label="URL",
        widget=forms.TextInput(attrs={"placeholder": "https://www.magmahealth.com"}),
    )

    promo_code = forms.CharField(
        label="Promo Code",
        widget=forms.TextInput(attrs={"placeholder": ""}),
        required=False,
    )

    class Meta:
        model = Company
        fields = ["name", "url"]


class CompanyFeatureForm(ModelForm):
    map_enabled = forms.BooleanField(
        label="Enabled / disable the display of your company map on the company home page",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600",
            }
        ),
    )

    links_enabled = forms.BooleanField(
        label="Enabled / disable the display of links on your company home page",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600",
            }
        ),
    )

    trivia_enabled = forms.BooleanField(
        label="Enabled / disable company trivia",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600",
            }
        ),
    )

    class Meta:
        model = Company
        fields = ["map_enabled", "links_enabled", "trivia_enabled"]


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


class BulkInviteRequestForm(ModelForm):
    file = forms.FileField(required=True, label="File", allow_empty_file=False)

    class Meta:
        model = BulkInviteRequest
        fields = ["file"]

    def __init__(self, *args, **kwargs):
        super(BulkInviteRequestForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs.update(
            {
                "class": FILE_FIELD_CLASS,
            }
        )


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
    color = ColorField()

    class Meta:
        model = Team
        fields = ["name", "color"]

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields["color"].widget.attrs.update({"class": "colorfield_field jscolor block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"})


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
