from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.core.files import File
from io import BytesIO
from pytils.translit import slugify
from PIL import Image
from customuser.models import User


class BlogCategory(models.Model):
    name = models.CharField('Название', max_length=120, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, editable=False, db_index=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)

class BlogPost(models.Model):
    category = models.ForeignKey(BlogCategory,on_delete=models.SET_NULL,blank=False,null=True)
    name = models.CharField('Название статьи', max_length=120, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, editable=False, db_index=True)
    image = models.ImageField('Изображение превью 200x200)', upload_to='article/', blank=False,null=True)
    image_post = models.ImageField('Изображение превью 200x200)', upload_to='article/', blank=False,null=True)
    title = models.CharField('TITLE', max_length=120, blank=False, null=True)
    description = models.TextField('DESCRIPTION', blank=False,null=True)
    short_description = models.TextField('Короткое описание', blank=False,null=True)
    text = RichTextUploadingField('Статья.', blank=False, null=True)
    views = models.IntegerField('Просмотров', default=0)
    is_active = models.BooleanField('Отображать статью ?', default=True, db_index=True)
    created_at = models.DateTimeField('Создана',auto_now_add=True)

    def get_preview_image(self):
        if self.image:
            return self.image.url
        else:
            return ''

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(BlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/blog/{self.name_slug}'

    def __str__(self):
        return f'id: {self.id} | Статья : {self.name}'

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

class BlogComment(models.Model):
    category = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    text = models.TextField(blank=False, null=True)

class BlogCommentComment(models.Model):
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    text = models.TextField(blank=False, null=True)





