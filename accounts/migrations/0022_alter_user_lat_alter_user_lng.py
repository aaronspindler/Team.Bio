# Generated by Django 4.2 on 2023-04-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_user_short_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
    ]
