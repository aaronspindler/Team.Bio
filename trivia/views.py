from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from trivia.models import TriviaQuestion, TriviaQuestionOption, TriviaUserAnswer


@login_required
def home(request):
    questions = TriviaQuestion.objects.filter(company=request.user.company).order_by("-created")

    for question in questions:
        question.options = question.question_option.all()
        question.selected_option = None
        for answer in question.user_answers.filter(user=request.user):
            question.selected_option = answer.selected_option
        question.disabled = ""
        if question.selected_option:
            question.disabled = "disabled"

    return render(request, "trivia/home.html", {"questions": questions})


@login_required
def answer_trivia_question(request, question):
    if request.method == "POST":
        question = get_object_or_404(TriviaQuestion, id=question)
        data = request.POST
        if request.user.company != question.company:
            print("User is not part of the company")
            return redirect("trivia_home")
        if TriviaUserAnswer.objects.filter(user=request.user, question=question).exists():
            print("User answer already exists")
            return redirect("trivia_home")
        answer = get_object_or_404(TriviaQuestionOption, text=data.get(question.question), question=question)
        TriviaUserAnswer.objects.create(user=request.user, question=question, selected_option=answer)
        return redirect("trivia_home")
