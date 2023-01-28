from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["email", "username", "company", "last_login"]


admin.site.register(User, UserAdmin)
