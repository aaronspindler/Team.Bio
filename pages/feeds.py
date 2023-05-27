from django.contrib.syndication.views import Feed

from pages.models import BlogPost


class BlogFeed(Feed):
    title = "Team Bio Blog"
    link = "/blog/feed"
    description = "Updates on changes and additions to Team Bio."

    def items(self):
        return BlogPost.objects.order_by("-created_at")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_content
