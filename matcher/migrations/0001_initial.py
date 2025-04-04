# Generated by Django 5.1.7 on 2025-03-26 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('resume_file', models.FileField(upload_to='resumes/')),
                ('skills', models.JSONField(default=list)),
                ('education', models.JSONField(default=list)),
                ('work_experience', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('required_skills', models.JSONField(default=list)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_score', models.IntegerField()),
                ('missing_skills', models.JSONField(default=list)),
                ('summary', models.TextField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matcher.candidateprofile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matcher.jobposting')),
            ],
        ),
    ]
