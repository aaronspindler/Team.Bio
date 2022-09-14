from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from companies.decorators import is_company_owner
from companies.forms import CompanyForm
from companies.models import CompanyOwner


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
def company_settings(request):
    company = request.user.company
    company_users = company.customuser_set.all()
    company_form = CompanyForm(instance=company)

    context = {
        'company_form': company_form,
        'company_users': company_users,
    }
    return render(request, 'companies/company_settings.html', context)


@login_required
def home(request):
    return render(request, 'companies/home.html')
