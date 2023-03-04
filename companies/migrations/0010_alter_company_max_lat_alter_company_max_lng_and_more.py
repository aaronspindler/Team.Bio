# Generated by Django 4.1.7 on 2023-03-04 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0009_company_max_lat_company_max_lng_company_min_lat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='max_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='max_lng',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='midpoint_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='midpoint_lng',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='min_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='min_lng',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
    ]
