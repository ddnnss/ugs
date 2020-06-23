# Generated by Django 2.2.7 on 2020-06-23 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0006_balancefreeze_bet_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='bet_result',
            field=models.BooleanField(blank=True, null=True, verbose_name='Результат'),
        ),
        migrations.AddField(
            model_name='bet',
            name='cashback',
            field=models.IntegerField(default=0, verbose_name='Возврат %'),
        ),
    ]
