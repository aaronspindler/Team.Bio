from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated and request.user.is_member_of_company:
        return redirect('company_home')
    return render(request, "pages/home.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def terms_of_service(request):
    return render(request, "pages/terms_of_service.html")
