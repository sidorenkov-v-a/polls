# Generated by Django 2.2.10 on 2021-08-01 22:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Poll title')),
                ('date_start', models.DateField(verbose_name='Date start')),
                ('date_end', models.DateField(verbose_name='Date end')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='polls.Poll', verbose_name='Poll')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Question text')),
                ('type', models.IntegerField(choices=[(1, 'Available text answer'), (2, 'Available only one choice'), (3, 'Available multiple choice')], verbose_name='Type of answer')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.Poll', verbose_name='Poll')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256, verbose_name='Choice text')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls.Question', verbose_name='Question choice')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Answer text')),
                ('choices', models.ManyToManyField(blank=True, related_name='answers', to='polls.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.Question', verbose_name='Question')),
                ('score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.Score', verbose_name='Question')),
            ],
        ),
    ]
