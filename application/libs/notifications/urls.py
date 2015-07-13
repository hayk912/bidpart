from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^goto/(?P<notification_id>\d+)/$', views.goto, name='goto'),
    url(r'^detail/(?P<notification_id>\d+)/$', views.detail, name='detail'),
)
