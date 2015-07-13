from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
   url(r'^(?P<slug>[-\w]+)/$', views.PageView.as_view(), name='page_view'),
)
