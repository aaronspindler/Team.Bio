from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import UserProfileForm
from accounts.models import User
from companies.decorators import is_company_owner
from companies.forms import CompanyForm, LocationForm
from companies.models import CompanyOwner, Company, Location, Team


@login_required
def create_company(request):
    # Check if the user already has a company, redirect them to the company page
    if request.user.companies.exists():
        return redirect('company_home')

    form = CompanyForm()
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            # Create a CompanyOwner object to track who owns the company
            CompanyOwner.objects.create(company=company, owner=request.user)

            # Update the users company field
            user = request.user
            user.company = company
            user.save()

            # After successful creation, redirect to the company page
            return redirect('company_home')

    return render(request, 'companies/create_company.html', {'form': form})


@login_required
@is_company_owner
def remove_user(request, email_prefix):
    user_to_remove = get_object_or_404(User, company=request.user.company, email_prefix=email_prefix)

    # Check if the user is a company owner
    if user_to_remove in request.user.company.get_owners:
        raise Http404

    # Deactivate the user
    if request.method == 'POST':
        user_to_remove.is_active = False
        user_to_remove.save()
        return redirect('company_settings')

    context = {
        'user_to_remove': user_to_remove
    }
    return render(request, 'companies/remove_user.html', context)


@login_required
@is_company_owner
def company_settings(request):
    company = request.user.company
    company_users = company.get_active_users
    company_form = CompanyForm(instance=company)

    locations = Location.objects.filter(company=company).order_by('name')

    teams = Team.objects.filter(company=company).order_by('name')

    context = {
        'company_form': company_form,
        'company_users': company_users,
        'locations': locations,
        'teams': teams,
    }
    return render(request, 'companies/company_settings.html', context)


@login_required
@is_company_owner
def add_location(request):
    form = LocationForm()
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.company = request.user.company
            instance.save()
            return redirect('company_settings')
    return render(request, 'companies/add_location.html', {'form': form})


@login_required
def user_profile(request, email_prefix):
    # Get the user requested for that company
    company_user = get_object_or_404(User, company=request.user.company, email_prefix=email_prefix)
    return render(request, 'companies/user_profile.html', {'company_user': company_user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', email_prefix=request.user.email_prefix)

    form = UserProfileForm(
        instance=request.user
    )

    return render(request, 'companies/edit_profile.html', {'form': form})


@login_required
def home(request):
    if request.user.company is None:
        # Check if there is a company with the URL root equal to the users email root
        company = Company.objects.filter(url_root=request.user.email_root)
        # If the company exists, make the user a member of that company
        if company:
            user = request.user
            user.company = company.first()
            user.save()
        else:
            return redirect('create_company')
    return render(request, 'companies/home.html')
