# Generated by Django 4.1.6 on 2023-02-03 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_user_zodiac_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_food',
            field=models.TextField(blank=True, null=True),
        ),
    ]
