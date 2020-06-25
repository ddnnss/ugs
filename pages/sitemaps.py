from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse



class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['index','about','contacts']

    def location(self, item):
        return reverse(item)



