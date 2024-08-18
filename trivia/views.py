from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from companies.decorators import is_company_owner
from trivia.models import (
    TriviaQuestion,
    TriviaQuestionGenerationRequest,
    TriviaQuestionOption,
    TriviaUserAnswer,
)
from trivia.tasks import generate_trivia_question


@login_required
def home(request):
    company = request.user.company
    if not company.trivia_enabled:
        return redirect("company_home")

    questions = TriviaQuestion.objects.filter(
        company=company, 
        published=True
    ).prefetch_related(
        Prefetch("question_option", to_attr="options"),
        Prefetch(
            "user_answers",
            queryset=TriviaUserAnswer.objects.filter(user=request.user),
            to_attr="user_answer"
        )
    ).order_by("-created")

    for question in questions:
        user_answer = question.user_answer[0] if question.user_answer else None
        question.selected_option = user_answer.selected_option if user_answer else None
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
    # Get all answers for the company
    all_answers = TriviaUserAnswer.objects.filter(
        question__published=True,
        question__company=request.user.company
    ).values('user__id', 'user__first_name', 'user__last_name', 'selected_option__correct')

    # Calculate total answers and correct answers for each user
    user_stats = {}
    for answer in all_answers:
        user_id = answer['user__id']
        if user_id not in user_stats:
            user_stats[user_id] = {
                'name': f"{answer['user__first_name']} {answer['user__last_name']}",
                'total_answers': 0,
                'correct_answers': 0
            }
        user_stats[user_id]['total_answers'] += 1
        if answer['selected_option__correct']:
            user_stats[user_id]['correct_answers'] += 1

    # Calculate accuracy and create results list
    results = []
    for user_id, stats in user_stats.items():
        accuracy = (stats['correct_answers'] / stats['total_answers']) * 100 if stats['total_answers'] > 0 else 0
        results.append({
            'name': stats['name'],
            'correct_answers': stats['correct_answers'],
            'total_answers': stats['total_answers'],
            'accuracy': round(accuracy, 2)
        })

    # Sort results by correct answers (descending) and then by accuracy (descending)
    results.sort(key=lambda x: (-x['correct_answers'], -x['accuracy']))

    return render(request, "trivia/leaderboard.html", {"leaderboard": results})


@login_required
@is_company_owner
def management(request):
    questions = TriviaQuestion.objects.filter(company=request.user.company).prefetch_related("question_option").order_by("-created", "-published")
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


@login_required
@is_company_owner
def publish_trivia_question(request, question):
    if request.method == "POST":
        question = get_object_or_404(TriviaQuestion, id=question, company=request.user.company)
        question.published = True
        question.save()
        messages.success(request, "Trivia question was successfully pubished")
        return redirect("trivia_management")
    return HttpResponseNotAllowed(["POST"])


@login_required
@is_company_owner
def edit_trivia_question(request, question):
    question = get_object_or_404(TriviaQuestion, id=question, company=request.user.company)
    if request.method == "POST":
        pass
    return render(request, "trivia/edit.html", {"question": question})


@login_required
@is_company_owner
def create_trivia_question(request):
    pass


@login_required
@is_company_owner
def generate_question(request):
    if request.method == "POST":
        if request.user.company.has_recently_generated_trivia_question():
            messages.error(request, "You have already generated a question recently, please wait a few minutes before generating another question")
        else:
            trivia_question_request = TriviaQuestionGenerationRequest.objects.create(company=request.user.company, requested_by=request.user)
            generate_trivia_question.delay(request.user.company.id, trivia_question_request.id)
            messages.success(request, "Trivia question is being generated, check back soon for your new question!")
        return redirect("trivia_management")
    return HttpResponseNotAllowed(["POST"])
