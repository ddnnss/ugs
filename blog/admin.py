from django.contrib import admin
from .models import *

admin.site.register(BlogPost)
admin.site.register(BlogCategory)
admin.site.register(BlogComment)
admin.site.register(BlogCommentComment)
