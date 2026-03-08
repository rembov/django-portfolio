from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "Мой блог - последние записи"
    link = "/blog/"
    description = "Свежие посты из моего блога"

    def items(self):
        return Post.objects.filter(published=True).order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:200]

    def item_link(self, item):
        return reverse('post_detail', args=[item.slug])