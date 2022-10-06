from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import CustomUser
from companies.decorators import is_company_owner
from companies.forms import CompanyForm
from companies.models import CompanyOwner, Company


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
def remove_user(request, user_to_remove):
    user_to_remove = get_object_or_404(CustomUser, company=request.user.company, email_prefix=user_to_remove)

    # Check if the user is a company owner
    if user_to_remove in request.user.company.get_owners():
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
    company_users = company.customuser_set.filter(is_active=True)
    company_form = CompanyForm(instance=company)

    context = {
        'company_form': company_form,
        'company_users': company_users,
    }
    return render(request, 'companies/company_settings.html', context)


@login_required
def user_profile(request, email_prefix):
    # Get the user requested for that company
    user = get_object_or_404(CustomUser, company=request.user.company, email_prefix=email_prefix)
    return render(request, 'companies/user_profile.html', {'user': user})


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
