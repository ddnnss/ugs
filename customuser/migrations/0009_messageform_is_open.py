# Generated by Django 2.2.7 on 2020-06-25 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0008_messageform'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageform',
            name='is_open',
            field=models.BooleanField(default=False),
        ),
    ]
