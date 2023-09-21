from django.contrib import admin

from .models import Pet, PetType, User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_filter = ["company"]
    list_display = ["email", "username", "company", "last_login", "profile_completion"]

    def profile_completion(self, obj):
        return f"{obj.profile_completion_percentage()}%"


class PetAdmin(admin.ModelAdmin):
    model = Pet
    list_display = ["name", "owner", "pet_type"]


class PetTypeAdmin(admin.ModelAdmin):
    model = PetType
    list_display = ["name"]


admin.site.register(User, UserAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(PetType, PetTypeAdmin)
