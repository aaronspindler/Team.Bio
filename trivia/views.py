from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from trivia.models import TriviaQuestion


@login_required
def trivia(request):
    questions = TriviaQuestion.objects.filter(company=request.user.company)
    questions = TriviaQuestion.objects.all()
    return render(request, "companies/trivia.html", {"questions": questions})
