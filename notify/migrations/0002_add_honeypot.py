# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_honeypot(apps, schema_editor):
    Destination = apps.get_model("notify", "Destination")
    try:
        obj = Destination.objects.get(name="honeypot")
    except Destination.DoesNotExist:
        obj = Destination(name="honeypot", email="honeypot")
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_honeypot),
    ]
