from django.contrib import admin

from pages.models import BlogPost, Tag


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ["name"]


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost
    list_display = ["title", "slug", "created_at", "edited_at"]

    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
