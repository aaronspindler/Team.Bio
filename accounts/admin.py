from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'company', 'last_login']


admin.site.register(CustomUser, CustomUserAdmin)
