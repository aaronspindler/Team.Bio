# Generated by Django 4.2 on 2023-04-18 15:45

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0017_company_promo_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
    ]
