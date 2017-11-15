# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

import unidecode as unidecode
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=45)
    slug = models.SlugField(default='')
    image = models.FileField(upload_to='django_meblyar/static/django_meblyar/img/categories/', blank=False,
                             null=True)

    def __str__(self):
        return self.name

    def slice_ref(self):
        ref = str(self.image)
        i = ref.find('img/')
        return ref[i:len(ref)]


class Subcategory(models.Model):
    name = models.CharField(max_length=45)
    extra_parameters = models.TextField(null=True)
    image = models.FileField(upload_to='django_meblyar/static/django_meblyar/img/subcategories/', blank=False,
                             null=True)
    slug = models.SlugField(default='')

    def __str__(self):
        return self.name

    def slice_ref(self):
        ref = str(self.image)
        i = ref.find('img/')
        return ref[i:len(ref)]

    def extra_to_dict(self):
        py_dict = json.loads(self.extra_parameters)
        return py_dict


class ProductFrom(models.Model):
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return u'%s: %s - %s' % (self.category_id, self.subcategory_id, self.subcategory_id.extra_parameters)


class Image(models.Model):
    JPEG = 'JPEG'
    PNG = 'PNG'
    IMAGE_EXTENSION = (
        (JPEG, 'jpeg'),
        (PNG, 'png'),
    )
    name = models.CharField(max_length=60)
    extension = models.CharField(max_length=4,
                                 choices=IMAGE_EXTENSION,
                                 default=JPEG)
    image = models.FileField(upload_to='django_meblyar/static/django_meblyar/img/products', blank=False, null=True)

    def __str__(self):
        return self.name

    def slice_ref(self):
        ref = str(self.image)
        i = ref.find('img/')
        return ref[i:len(ref)]


class Product(models.Model):
    title = models.CharField(max_length=50)
    image = models.ManyToManyField(Image)
    from_id = models.ForeignKey(ProductFrom, on_delete=models.PROTECT)
    extra_parameters_json = models.TextField(null=True)
    slug_params_json = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    # for creating sluged json-like field
    def save(self):
        extra_dict = json.loads(self.extra_parameters_json)
        slug_extra_list = []
        for key, value in extra_dict.items():
            uni_key = unidecode.unidecode(key).lower()
            sluged_key = re.sub(r'\W+', '-', uni_key)

            uni_value = unidecode.unidecode(value).lower()
            sluged_value = re.sub(r'\W+', '-', uni_value)

            slug_extra_list.append(sluged_key + '=' + sluged_value)
        self.slug_params_json = slug_extra_list
        super(Product, self).save()

    def extra_to_dict(self):
        py_dict = json.loads(self.extra_parameters_json)
        return py_dict
