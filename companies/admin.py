from django.contrib import admin

from companies.models import Company, CompanyOwner


class CompanyAdmin(admin.ModelAdmin):
    model = Company


class CompanyOwnerAdmin(admin.ModelAdmin):
    model = CompanyOwner


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyOwner, CompanyOwnerAdmin)
