from django.contrib import admin

from companies.models import Company


class CompanyAdmin(admin.ModelAdmin):
    model = Company


admin.site.register(Company, CompanyAdmin)
