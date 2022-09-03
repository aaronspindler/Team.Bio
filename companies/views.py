from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from companies.forms import CompanyCreationForm
from companies.models import CompanyOwner


@login_required
def create_company(request):
    # Check if the user already has a company, redirect them to the company page
    if request.user.companies.exists():
        return redirect('company_home')

    form = CompanyCreationForm()
    if request.method == "POST":
        form = CompanyCreationForm(request.POST)
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
def company_admin(request):
    return render(request, 'companies/company_admin.html')


@login_required
def home(request):
    return render(request, 'companies/home.html')
