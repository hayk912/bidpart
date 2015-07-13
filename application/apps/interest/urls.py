from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^success', views.InterestSuccess.as_view(), name='success'),
    url(r'^', views.InterestCreateView.as_view(), name='create'),
)
