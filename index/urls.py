from django.conf.urls import url

from index.views import IndexPage
from . import views

urlpatterns = [
    url(r'^$', IndexPage.as_view(), name='index'),
    url(r'^services/$', views.services, name='services'),
    url(r'^contact/$', views.contact, name='contact'),
]
