# Generated by Django 4.1.5 on 2023-01-28 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_remove_company_payment_failed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='test_company',
            field=models.BooleanField(default=False),
        ),
    ]
