from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    title = models.TextField()
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=255)

    thumbnail = models.ImageField(blank=True, null=True, upload_to="blog/")
    tags = models.ManyToManyField("Tag", blank=True)

    short_content = models.TextField(blank=True, null=True)
    content_html = models.TextField(blank=True, null=True)

    posted_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("blog_post", args=[str(self.slug)])


class Tag(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name
