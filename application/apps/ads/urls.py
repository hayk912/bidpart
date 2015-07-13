from django.conf.urls import patterns, url
from . import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^ad/(?P<pk>\d+)/$', views.AdView.as_view(), name='ad_detail'),
    url(r'^create/$', views.AdCreateView.as_view(), name='ad_create'),
    url(r'^update/(?P<pk>\d+)/$', views.AdUpdateView.as_view(),
        name='ad_update'),
    url(r'^delete/(?P<pk>\d+)/$', views.AdDeleteView.as_view(),
        name='ad_delete'),
    url(r'^delete/success/$', TemplateView.as_view(template_name='ads/ad_success_delete.html'),
        name='ad_success_delete'),


    url(r'^ad_api/product_type_fields/(?P<product_type>\d+)/(?P<is_request>\d+)$', views.get_product_type_fields, name='get_product_type_fields'),
    url(r'^ad_api/product_type_fields/(?P<product_type>\d+)/$', views.get_product_type_fields, name='get_product_type_fields'),
    url(r'^ad_api/product_types/(?P<product_category>\d+)/$', views.get_product_types, name='get_product_types'),

    url(r'^ad_api/upload_image/$', views.AdImageCreateView.as_view(), name='upload_image'),
    url(r'^ad_api/upload_file/$', views.AdFileCreateView.as_view(), name='upload_file'),
    url(r'^ad_api/get_provision/$', views.GetBidpartProvisionView.as_view(), name='get_provision'),

    url(r'^show_buy_sell/(?P<show>\w+)/$', views.show_buy_sell, name='show_buy_sell'),

    url(r'^([\w\d\-_]+)/([\w\d\-_]+)/([\w\d\-_]+)/$', views.AdsListView.as_view(), name='ad_filter'),
    url(r'^([\w\d\-_]+)/([\w\d\-_]+)/$', views.AdsListView.as_view(), name='ad_filter'),
    url(r'^([\w\d\-_]+)/$', views.AdsListView.as_view(), name='ad_filter'),
    url(r'^$', views.AdsListView.as_view(), name='ad_filter')
)
