# Generated by Django 4.2.5 on 2023-09-20 00:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='triviaquestion',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triviaquestion',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
