import urllib.parse

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from accounts.forms import PetForm, UserProfileForm
from accounts.models import Pet, User
from billing.models import PromoCode
from companies.decorators import is_company_owner
from companies.forms import (
    CompanyFeatureForm,
    CompanyForm,
    InviteForm,
    LinkForm,
    LocationForm,
    TeamForm,
)
from companies.models import Company, CompanyOwner, Invite, Link, Location, Team
from utils.models import Email


@login_required
def create_company(request):
    # Check if the user already has a company, redirect them to the company page
    if request.user.companies.exists():
        return redirect("company_home")

    form = CompanyForm()
    if request.method == "POST":
        form = CompanyForm(data=request.POST)
        if form.is_valid():
            company = form.save()
            # Create a CompanyOwner object to track who owns the company
            CompanyOwner.objects.create(company=company, owner=request.user)

            promo_code = form.cleaned_data.get("promo_code")
            if promo_code:
                # check if the promo code exists
                promo_code = PromoCode.objects.filter(code=promo_code)
                # if the promo code exists set the companies trial days to the promo code amount
                if promo_code:
                    company.trial_days = promo_code.first().num_free_days
                    company.save()

            # Update the users company field
            user = request.user
            user.company = company
            user.save()

            # After successful creation, redirect to the company page
            return redirect("company_home")

    return render(request, "companies/create_company.html", {"form": form})


@login_required
@is_company_owner
def invite(request):
    form = InviteForm()
    if request.method == "POST":
        form = InviteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            email = instance.email.lower()
            # Check if this user already exists as a user or a previous invite
            if (
                not User.objects.filter(email=email).exists()
                and not Invite.objects.filter(email=email).exists()
            ):
                instance.email = email
                instance.company = request.user.company
                instance.save()

                # Send an invitation email
                email = Email.objects.create(
                    recipient=instance.email,
                    template="invite",
                    subject=f"You have been invited by {request.user.name} to join your co-workers on Team Bio",
                )
                parameters = {
                    "invite_sender_name": request.user.name,
                    "invite_sender_organization_name": request.user.company.name,
                    "action_url": f"https://www.team.bio{reverse('account_signup')}",
                }
                email.send(parameters)
            return redirect("company_settings")
    return render(request, "companies/invite.html", {"form": form})


@login_required
@is_company_owner
def revoke_invite(request, email):
    email = str(email)
    invite = get_object_or_404(Invite, company=request.user.company, email=email)
    if request.method == "POST":
        invite.delete()
        return redirect("company_settings")


@login_required
@is_company_owner
def remove_user(request, email_prefix):
    user_to_remove = get_object_or_404(
        User, company=request.user.company, email_prefix=email_prefix
    )

    # Check if the user is a company owner
    if user_to_remove in request.user.company.get_owners:
        raise Http404

    # Deactivate the user
    if request.method == "POST":
        user_to_remove.is_active = False
        user_to_remove.save()
        return redirect("company_settings")

    context = {"user_to_remove": user_to_remove}
    return render(request, "companies/remove_user.html", context)


@login_required
@is_company_owner
def company_settings(request):
    company = request.user.company
    company_users = company.get_active_users
    invited_users = company.get_invited_users

    locations = (
        Location.objects.filter(company=company)
        .order_by("name")
        .annotate(Count("user", distinct=True))
    )
    teams = (
        Team.objects.filter(company=company)
        .order_by("name")
        .annotate(Count("user", distinct=True))
    )
    links = Link.objects.filter(company=company).order_by("name")

    billing_user = company.get_billing_user
    billing_email = None
    manage_billing_link = None
    if billing_user:
        billing_email = billing_user.user.email
        manage_billing_link = "https://billing.stripe.com/p/login/4gw8zp2YTeZmcta288"
        url_parameters = urllib.parse.urlencode({"prefilled_email": billing_email})
        manage_billing_link += f"?{url_parameters}"

    company_feature_form = CompanyFeatureForm(instance=company)
    if request.method == "POST":
        company_feature_form = CompanyFeatureForm(request.POST, instance=company)
        if company_feature_form.is_valid():
            company_feature_form.save()

    context = {
        "owners": company.get_owners,
        "company_users": company_users,
        "invited_users": invited_users,
        "locations": locations,
        "teams": teams,
        "links": links,
        "billing_email": billing_email,
        "manage_billing_link": manage_billing_link,
        "company_feature_form": company_feature_form,
    }
    return render(request, "companies/company_settings.html", context)


@login_required
@is_company_owner
def make_owner(request, email_prefix):
    user = get_object_or_404(
        User, company=request.user.company, email_prefix=email_prefix
    )

    # Check if the user is already an owner
    if user in request.user.company.get_owners:
        raise Http404

    # Make the user an owner
    if request.method == "POST":
        CompanyOwner.objects.create(company=request.user.company, owner=user)

    return redirect("company_settings")


@login_required
@is_company_owner
def remove_owner(request, email_prefix):
    user = get_object_or_404(
        User, company=request.user.company, email_prefix=email_prefix
    )

    # Check if the user is already an owner
    if user not in request.user.company.get_owners:
        raise Http404

    if user == request.user:
        raise Http404

    # Remove the user as an owner
    if request.method == "POST":
        CompanyOwner.objects.filter(company=request.user.company, owner=user).delete()

    return redirect("company_settings")


@login_required
@is_company_owner
def add_location(request):
    form = LocationForm()
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Check if this already exists
            if not Location.objects.filter(
                company=request.user.company, name=instance.name
            ).exists():
                instance.company = request.user.company
                instance.save()
            return redirect("company_settings")
    return render(request, "companies/add_location.html", {"form": form})


@login_required
@is_company_owner
def delete_location(request, pk):
    if request.method == "POST":
        company = request.user.company
        location = get_object_or_404(Location, pk=pk, company=company)
        # Find users that are in this location and remove them from the location
        # This prevents any cascading deletes
        User.objects.filter(company=company, general_location=location).update(
            general_location=None
        )
        location.delete()
        return redirect("company_settings")


@method_decorator(login_required, name="dispatch")
@method_decorator(is_company_owner, name="dispatch")
class UpdateLocationView(UpdateView):
    model = Location
    template_name = "companies/update_location.html"
    success_url = reverse_lazy("company_settings")
    form_class = LocationForm

    def get_object(self, *args, **kwargs):
        obj = super(UpdateLocationView, self).get_object(*args, **kwargs)
        if obj.company != self.request.user.company:
            raise Http404
        return obj


@login_required
@is_company_owner
def add_team(request):
    form = TeamForm()
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Check if this already exists
            if not Team.objects.filter(
                company=request.user.company, name=instance.name
            ).exists():
                instance.company = request.user.company
                instance.save()
            return redirect("company_settings")
    return render(request, "companies/add_team.html", {"form": form})


@login_required
@is_company_owner
def delete_team(request, pk):
    if request.method == "POST":
        company = request.user.company
        team = get_object_or_404(Team, company=company, pk=pk)
        # Find users that are in this team and remove them from the team
        User.objects.filter(company=company, team=team).update(team=None)
        team.delete()
        return redirect("company_settings")


@method_decorator(login_required, name="dispatch")
@method_decorator(is_company_owner, name="dispatch")
class UpdateTeamView(UpdateView):
    model = Team
    template_name = "companies/update_team.html"
    success_url = reverse_lazy("company_settings")
    form_class = TeamForm

    def get_object(self, *args, **kwargs):
        obj = super(UpdateTeamView, self).get_object(*args, **kwargs)
        if obj.company != self.request.user.company:
            raise Http404
        return obj


@login_required
def user_profile(request, email_prefix):
    # Get the user requested for that company
    company_user = get_object_or_404(
        User, company=request.user.company, email_prefix=email_prefix
    )

    pets = Pet.objects.filter(owner=company_user)

    is_profile_owner = False
    if company_user == request.user:
        is_profile_owner = True

    return render(
        request,
        "companies/user_profile.html",
        {
            "company_user": company_user,
            "pets": pets,
            "is_profile_owner": is_profile_owner,
        },
    )


@login_required
def edit_profile(request):
    company = request.user.company
    form = UserProfileForm(instance=request.user, company=company)
    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user, company=company
        )
        if form.is_valid():
            form.save()
            company.calculate_geo_midpoint()
            company.calculate_map_bounds()
            return redirect("user_profile", email_prefix=request.user.email_prefix)
        print(form.errors)

    return render(request, "companies/edit_profile.html", {"form": form})


@login_required
@is_company_owner
def add_link(request):
    form = LinkForm()
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Check if this already exists
            if not Link.objects.filter(
                company=request.user.company, name=instance.name
            ).exists():
                instance.company = request.user.company
                instance.save()
            return redirect("company_settings")
    return render(request, "companies/add_link.html", {"form": form})


@login_required
@is_company_owner
def delete_link(request, pk):
    if request.method == "POST":
        company = request.user.company
        link = get_object_or_404(Link, company=company, pk=pk)
        link.delete()
        return redirect("company_settings")


@login_required
def add_pet(request):
    user = request.user
    form = PetForm()
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.save()
            return redirect(user.profile_url)
    return render(request, "companies/add_pet.html", {"form": form})


@login_required
def delete_pet(request, pk):
    user = request.user
    if request.method == "POST":
        pet = get_object_or_404(Pet, owner=request.user, pk=pk)
        pet.delete()
        return redirect(user.profile_url)
    return Http404


@method_decorator(login_required, name="dispatch")
class UpdatePetView(UpdateView):
    model = Pet
    template_name = "companies/update_pet.html"
    success_url = reverse_lazy("edit_profile")
    form_class = PetForm

    def get_object(self, *args, **kwargs):
        obj = super(UpdatePetView, self).get_object(*args, **kwargs)
        if obj.owner != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy(
            "user_profile", kwargs={"email_prefix": self.request.user.email_prefix}
        )


@login_required
def home(request):
    user = request.user
    company = request.user.company
    if company is None:
        # Check if there is a company with the URL root equal to the users email root
        check_company = Company.objects.filter(url_root=user.email_root)
        # If the company exists, make the user a member of that company
        if check_company:
            user.company = check_company.first()
            company = user.company
            user.save()
        else:
            return redirect("create_company")

    # If the user is a company owner and their billing is inactive, redirect them to the settings page
    if user in company.get_owners and company.is_enabled is False:
        return redirect("company_settings")
    # if the user is not a company owner and their billing is inactive, redirect them to billing inactive page
    elif user not in company.get_owners and company.is_enabled is False:
        return redirect("billing_inactive")

    data = {}
    data.update(company.get_map_data())
    data.update(company.get_link_data())

    return render(request, "companies/home.html", data)
