# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from catalog.models import Category, Subcategory, Product, ProductFrom, Image


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/jquery-latest.min.js',
            'js/adminscripts.js',
        )
    # prepopulated_fields = {'slug_params_json': ('extra_parameters_json', )}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubCategoryAdmin)
admin.site.register(ProductFrom)
admin.site.register(Image)
