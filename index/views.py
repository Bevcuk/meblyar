# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from catalog.models import Subcategory, ProductFrom, Category


def services(request):
    return render(request, 'services.html', {})


class IndexPage(ListView):
    template_name = "index.html"
    paginate_by = 24

    def get_queryset(self, *args, **kwargs):
        queryset = Subcategory.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(IndexPage, self).get_context_data()
        context['plutni'] =ProductFrom.objects.filter(category_id__slug='plitni-materiali')
        context['category'] =Category.objects.all()
        context['category_all'] = Category.objects.all()
        # context['extra_params'] = Subcategory.objects.get(slug=self.kwargs['subcategory_slug'])
        if self.get_queryset().count() == 1:
            context['single_queryset'] = True
        return context
