# Generated by Django 4.2.5 on 2023-09-20 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_gptmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='gptmodel',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]