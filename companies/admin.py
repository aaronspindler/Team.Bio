from django.contrib import admin

from companies.models import (
    BulkInviteRequest,
    Company,
    CompanyOwner,
    Invite,
    Link,
    Location,
    Team,
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


@admin.register(BulkInviteRequest)
class BulkInviteRequestAdmin(admin.ModelAdmin):
    list_display = ["company", "created", "file", "processed"]
    list_filter = ["company"]
    model = BulkInviteRequest
