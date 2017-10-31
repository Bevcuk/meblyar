# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('extension', models.CharField(choices=[('JPEG', 'jpeg'), ('PNG', 'png')], default='JPEG', max_length=4)),
                ('image', models.FileField(null=True, upload_to='django_meblyar/static/django_meblyar/img/products')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('extra_parameters_json', models.TextField(null=True)),
                ('slug_params_json', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductFrom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('extra_parameters', models.TextField(null=True)),
                ('image', models.FileField(null=True, upload_to='django_meblyar/static/django_meblyar/img/subcategories/')),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='productfrom',
            name='subcategory_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.Subcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='from_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.ProductFrom'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(to='catalog.Image'),
        ),
    ]