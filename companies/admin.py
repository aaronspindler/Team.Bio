from django.contrib import admin

from companies.models import Company, CompanyOwner, Invite, Location, Team


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company


@admin.register(CompanyOwner)
class CompanyOwnerAdmin(admin.ModelAdmin):
    model = CompanyOwner


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    model = Location


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    model = Team


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    model = Invite
