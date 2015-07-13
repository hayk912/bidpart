from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^(?P<identifier>[\w]+)$', views.index, name='index'),
)
