from django.urls import path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.posts, name='posts'),
    path('<article_name_slug>', views.post, name='post'),
   


]