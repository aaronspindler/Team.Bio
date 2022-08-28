from django.shortcuts import render, redirect


def home(request):
    if request.user.is_member_of_company:
        return redirect('company_home')
    return render(request, "pages/home.html")
