# Generated by Django 2.1.4 on 2020-08-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0014_auto_20200723_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='user',
            name='billing_address',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='user',
            name='billing_country',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='user',
            name='billing_house',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Дом'),
        ),
        migrations.AddField(
            model_name='user',
            name='billing_post',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Индекс'),
        ),
        migrations.AddField(
            model_name='user',
            name='billing_town',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_add',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Эл. почта'),
        ),
        migrations.AddField(
            model_name='user',
            name='house',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Дом'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_add',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='user',
            name='town',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Город'),
        ),
    ]