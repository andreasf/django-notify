# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import notify.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(default=notify.models.create_challenge, unique=True, max_length=64)),
                ('valid_until', models.DateTimeField(default=notify.models.default_validity)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('key', models.CharField(default=notify.models.create_key, max_length=512)),
                ('email', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='destination',
            field=models.ForeignKey(to='notify.Destination'),
        ),
    ]
