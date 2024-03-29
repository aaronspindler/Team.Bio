# Generated by Django 4.1.7 on 2023-03-22 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_company_map_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('url', models.URLField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='companies.company')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
                'unique_together': {('company', 'name')},
            },
        ),
    ]
