from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from companies.decorators import is_company_owner
from trivia.models import TriviaQuestion, TriviaQuestionOption, TriviaUserAnswer


@login_required
def home(request):
    company = request.user.company
    if not company.trivia_enabled:
        return redirect("company_home")

    user_answers_prefetch = Prefetch("user_answers", queryset=TriviaUserAnswer.objects.filter(user=request.user), to_attr="user_answer")
    questions = TriviaQuestion.objects.filter(company=company, published=True).prefetch_related(Prefetch("question_option", to_attr="options"), user_answers_prefetch).order_by("-created")

    for question in questions:
        question.selected_option = question.user_answer[0].selected_option if question.user_answer else None
        question.disabled = "disabled" if question.selected_option else ""

    return render(request, "trivia/home.html", {"questions": questions})


@login_required
def answer_trivia_question(request, question):
    if request.method == "POST":
        question = get_object_or_404(TriviaQuestion, id=question, published=True)
        data = request.POST
        if request.user.company != question.company:
            print("User is not part of the company")
            return redirect("trivia_home")
        if TriviaUserAnswer.objects.filter(user=request.user, question=question).exists():
            print("User answer already exists")
            return redirect("trivia_home")
        answer = get_object_or_404(TriviaQuestionOption, text=data.get(str(question.pk)), question=question)
        TriviaUserAnswer.objects.create(user=request.user, question=question, selected_option=answer)
        return redirect("trivia_home")
    return HttpResponseNotAllowed(["POST"])


@login_required
def leaderboard(request):
    leaderboard = TriviaUserAnswer.objects.filter(question__published=True, selected_option__correct=True, question__company=request.user.company).values("user__first_name", "user__last_name").annotate(correct_answers=Count("id")).order_by("-correct_answers")

    results = []
    for row in leaderboard:
        results.append({"name": f'{row["user__first_name"]} {row["user__last_name"]}', "correct_answers": row["correct_answers"]})

    return render(request, "trivia/leaderboard.html", {"leaderboard": results})


@login_required
@is_company_owner
def management(request):
    questions = TriviaQuestion.objects.filter(company=request.user.company).order_by("-created", "-published")
    return render(request, "trivia/management.html", {"questions": questions})


@login_required
@is_company_owner
def delete_trivia_question(request, question):
    if request.method == "POST":
        question = get_object_or_404(TriviaQuestion, id=question, company=request.user.company)
        question.delete()
        messages.success(request, "Trivia question was successfully deleted")
        return redirect("trivia_management")
    return HttpResponseNotAllowed(["POST"])
