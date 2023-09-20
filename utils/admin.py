from django.contrib import admin

from utils.models import AdminEmail, AdminPhoneNumber, Email, GPTModel, TextMessage


class EmailAdmin(admin.ModelAdmin):
    model = Email
    list_filter = ["sent"]
    list_display = ["recipient", "subject", "sent"]


class TextMessageAdmin(admin.ModelAdmin):
    model = TextMessage
    list_filter = ["sent"]
    list_display = ["recipient", "sent"]

    actions = ["send_text"]

    @admin.action(description="Send text message(s)")
    def send_text(self, request, queryset):
        for message in queryset:
            message.send()


admin.site.register(TextMessage, TextMessageAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(AdminPhoneNumber)
admin.site.register(AdminEmail)
admin.site.register(GPTModel)
