# Generated by Django 4.2.2 on 2023-06-18 02:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0018_team_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriviaQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trivia_questions', to='companies.company')),
            ],
            options={
                'verbose_name': 'Trivia Question',
                'verbose_name_plural': 'Trivia Questions',
            },
        ),
        migrations.CreateModel(
            name='TriviaQuestionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trivia_answers', to='companies.triviaquestion')),
            ],
            options={
                'verbose_name': 'Trivia Question Option',
                'verbose_name_plural': 'Trivia Question Options',
            },
        ),
        migrations.CreateModel(
            name='TriviaUserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='companies.triviaquestion')),
                ('selected_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='companies.triviaquestionoption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trivia_answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Trivia User Answer',
                'verbose_name_plural': 'Trivia User Answers',
                'unique_together': {('user', 'question')},
            },
        ),
    ]
