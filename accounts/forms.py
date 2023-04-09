from django import forms

from accounts.models import Pet, User
from companies.models import Location, Team

basic_field_class = "block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"


class PetForm(forms.ModelForm):
    picture = forms.ImageField(label="", required=False)

    class Meta:
        model = Pet
        fields = ["name", "nickname", "pet_type", "picture"]

    def __init__(self, *args, **kwargs):
        super(PetForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": basic_field_class})
        self.fields["nickname"].widget.attrs.update({"class": basic_field_class})
        self.fields["pet_type"].widget.attrs.update({"class": basic_field_class})
        self.fields["picture"].widget.attrs.update(
            {
                "class": "rounded-md border border-gray-300 bg-white text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            }
        )


class UserProfileForm(forms.ModelForm):
    short_bio = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": "3"})
    )
    favourite_food = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": "2"})
    )
    favourite_movie = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": "2"})
    )
    favourite_travel_destination = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": "2"})
    )
    profile_picture = forms.ImageField(label="", required=False)

    class Meta:
        model = User
        fields = [
            "profile_picture",
            "short_bio",
            "first_name",
            "last_name",
            "title",
            "general_location",
            "team",
            "personality_type",
            "linkedin",
            "twitter",
            "github",
            "chinese_zodiac",
            "zodiac_sign",
            "favourite_food",
            "favourite_movie",
            "favourite_travel_destination",
            "address_1",
            "city",
            "prov_state",
            "postal_code",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company")
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields["general_location"].queryset = Location.objects.filter(
            company=company
        )
        self.fields["general_location"].widget.attrs.update(
            {"class": basic_field_class}
        )

        self.fields["team"].queryset = Team.objects.filter(company=company)
        self.fields["team"].widget.attrs.update({"class": basic_field_class})

        self.fields["personality_type"].widget.attrs.update(
            {"class": basic_field_class}
        )

        self.fields["chinese_zodiac"].widget.attrs.update({"class": basic_field_class})

        self.fields["zodiac_sign"].widget.attrs.update({"class": basic_field_class})

        self.fields["favourite_food"].widget.attrs.update({"class": basic_field_class})

        self.fields["favourite_movie"].widget.attrs.update({"class": basic_field_class})

        self.fields["favourite_travel_destination"].widget.attrs.update(
            {"class": basic_field_class}
        )

        self.fields["title"].widget.attrs.update({"class": basic_field_class})

        self.fields["short_bio"].widget.attrs.update({"class": basic_field_class})

        self.fields["linkedin"].widget.attrs.update(
            {
                "class": "block w-full min-w-0 flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            }
        )

        self.fields["twitter"].widget.attrs.update(
            {
                "class": "block w-full min-w-0 flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            }
        )

        self.fields["github"].widget.attrs.update(
            {
                "class": "block w-full min-w-0 flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            }
        )

        self.fields["first_name"].widget.attrs.update({"class": basic_field_class})

        self.fields["last_name"].widget.attrs.update({"class": basic_field_class})

        self.fields["address_1"].widget.attrs.update(
            {
                "class": basic_field_class,
                "autocomplete": "street-address",
            }
        )
        self.fields["city"].widget.attrs.update(
            {
                "class": basic_field_class,
                "autocomplete": "city",
            }
        )
        self.fields["prov_state"].widget.attrs.update(
            {
                "class": basic_field_class,
                "autocomplete": "state",
            }
        )
        self.fields["postal_code"].widget.attrs.update(
            {
                "class": basic_field_class,
                "autocomplete": "country",
            }
        )
        self.fields["country"].widget.attrs.update(
            {
                "class": basic_field_class,
                "autocomplete": "postal-code",
            }
        )

        self.fields["profile_picture"].widget.attrs.update(
            {
                "class": "rounded-md border border-gray-300 bg-white text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            }
        )
