from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.BlogListView.as_view(), name='blog_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.BlogDetailView.as_view(), name='blog_view'),
)
