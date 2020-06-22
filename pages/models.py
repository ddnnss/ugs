from django.db import models

class Faq(models.Model):
    title = models.CharField('Вопрос',max_length=255,blank=True,null=True)
    text = models.TextField('Ответ',blank=True,null=True)
    is_first = models.BooleanField('Отображается на главной?', default=False)

class Feedback(models.Model):
    name = models.CharField('От',max_length=255,blank=True,null=True)
    profession = models.CharField('Профессия',max_length=255,blank=True,null=True)
    text = models.TextField('Отзыв',blank=True,null=True)
    avatar = models.ImageField('Фото от', upload_to='feedback/', blank=True)