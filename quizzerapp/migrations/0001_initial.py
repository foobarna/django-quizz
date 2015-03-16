# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.CharField(max_length=500)),
                ('score', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('page', models.ForeignKey(to='quizzerapp.Page')),
            ],
            options={
                'ordering': ['weight'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionnairePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('page', models.ForeignKey(to='quizzerapp.Page')),
                ('questionnaire', models.ForeignKey(to='quizzerapp.Questionnaire')),
            ],
            options={
                'ordering': ['weight'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result_text', models.CharField(max_length=1000)),
                ('upper_limit', models.IntegerField(default=0)),
                ('questionnaire', models.ForeignKey(to='quizzerapp.Questionnaire')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='pages',
            field=models.ManyToManyField(to='quizzerapp.Page', through='quizzerapp.QuestionnairePage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagequestion',
            name='question',
            field=models.ForeignKey(to='quizzerapp.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='questions',
            field=models.ManyToManyField(to='quizzerapp.Question', through='quizzerapp.PageQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='quizzerapp.Question'),
            preserve_default=True,
        ),
    ]
