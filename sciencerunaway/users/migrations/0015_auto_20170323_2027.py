# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20170311_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]