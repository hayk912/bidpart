from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^optout', views.EdrOptoutView.as_view(), name='optout'),
    url(r'^success', views.EdrOptOutSuccess.as_view(), name='success'),
)
