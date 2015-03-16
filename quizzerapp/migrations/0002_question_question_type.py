# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzerapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(default=b'sg', max_length=2, choices=[(b'sg', b'Single answer'), (b'mp', b'Multiple answers')]),
            preserve_default=True,
        ),
    ]
