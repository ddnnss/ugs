from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse



class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return ['index','about','contacts']

    def location(self, item):
        return reverse(item)



