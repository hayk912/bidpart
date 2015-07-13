from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^create', views.DealsCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', views.DealsUpdateView.as_view(), name='update'),
)
