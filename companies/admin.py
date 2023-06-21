from django.contrib import admin

from companies.models import (
    Company,
    CompanyOwner,
    Invite,
    Link,
    Location,
    Team,
    TriviaQuestion,
    TriviaQuestionOption,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company


@admin.register(CompanyOwner)
class CompanyOwnerAdmin(admin.ModelAdmin):
    model = CompanyOwner


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["company", "name"]
    list_filter = ["company"]
    model = Location


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["company", "name"]
    list_filter = ["company"]
    model = Team


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ["company", "email"]
    list_filter = ["company"]
    model = Invite


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["company", "name"]
    list_filter = ["company"]
    model = Link


@admin.register(TriviaQuestion)
class TriviaQuestionAdmin(admin.ModelAdmin):
    list_display = ["company", "question"]
    list_filter = ["company"]
    model = TriviaQuestion


@admin.register(TriviaQuestionOption)
class TriviaQuestionOption(admin.ModelAdmin):
    list_display = ["question", "text", "correct"]
    list_filter = ["question"]
    model = TriviaQuestionOption
