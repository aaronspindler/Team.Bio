# Generated by Django 4.1.2 on 2022-10-15 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_team_location'),
        ('accounts', '0007_customuser_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='general_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.location'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.team'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_picture/'),
        ),
    ]
