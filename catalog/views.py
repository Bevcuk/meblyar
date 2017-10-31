# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import operator
import re
from functools import reduce

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from catalog.models import Product, ProductFrom, Subcategory, Category


def catalog(request):
    return render(request, 'catalog/catalog.html', {})


class ProductsPage(ListView):
    template_name = "catalog/catalog.html"
    paginate_by = 24

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(from_id__subcategory_id__slug=self.kwargs['subcategory_slug'])
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProductsPage, self).get_context_data()

        # pagination part
        products_list = self.get_queryset()
        paginator = Paginator(products_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            page_set = paginator.page(page)
        except PageNotAnInteger:
            page_set = paginator.page(1)
        except EmptyPage:
            page_set = paginator.page(paginator.num_pages)

        context['products'] = page_set
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        # context['category'] = ProductFrom.objects.filter(subcategory_id__slug=self.kwargs['subcategory_slug']).first()
        subcategory = ProductFrom.objects.filter(category_id__slug=self.kwargs['category_slug'])
        context['subcategories'] = subcategory
        context['extra_params'] = Subcategory.objects.get(slug=self.kwargs['subcategory_slug'])
        # context['extra_params'] = Subcategory.objects.get(slug=self.kwargs['subcategory_slug'])
        if self.get_queryset().count() == 1:
            context['single_queryset'] = True
        return context


class FilteredProductsPage(ListView):
    template_name = "catalog/catalog.html"
    paginate_by = 24

    def get_queryset(self, *args, **kwargs):
        extra = self.kwargs['extra_params']
        search_list = extra.split(';')
        full_search_list = []
        queryset = Product.objects.filter(from_id__subcategory_id__slug=self.kwargs['subcategory_slug'])
        search_list_flat = [re.split(r'[=_]+', i) for i in search_list]
        search_dict = {item[0]: item[1:] for item in search_list_flat}
        # to have [['frictsion=4-2', 'frictsion=3-4'], ['brand=calm3', 'brand=colo']]

        for key, value in search_dict.items():
            full_search_list.append([key + '=' + i for i in value])

        for param in full_search_list:
            queryset = queryset.filter(reduce(operator.or_, (Q(slug_params_json__contains=item) for item in param)))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(FilteredProductsPage, self).get_context_data()

        # pagination part
        products_list = self.get_queryset()
        paginator = Paginator(products_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            page_set = paginator.page(page)
        except PageNotAnInteger:
            page_set = paginator.page(1)
        except EmptyPage:
            page_set = paginator.page(paginator.num_pages)

        context['products'] = page_set

        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        subcategory = ProductFrom.objects.filter(category_id__slug=self.kwargs['category_slug'])
        context['subcategories'] = subcategory
        context['extra_params'] = Subcategory.objects.get(slug=self.kwargs['subcategory_slug'])
        if self.get_queryset().count() == 1:
            context['single_queryset'] = True
        return context
