# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.FileField(null=True, upload_to='django_meblyar/static/django_meblyar/img/categories/'),
        ),
    ]
