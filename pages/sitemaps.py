from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import BlogPost


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return ['index','about','contacts']

    def location(self, item):
        return reverse(item)



class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return BlogPost.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at