from django.conf.urls import url

from index.views import IndexPage
from . import views

urlpatterns = [
    url(r'^$', IndexPage.as_view(), name='index'),
]
