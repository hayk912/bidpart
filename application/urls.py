from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

#noinspection PyPackageRequirements
urlpatterns = patterns('',
    # Examples:
    # url(r'^application/', include('application.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^accounts/', include('application.apps.accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^currencies/', include('currencies.urls')),

    url(r'^notifications/', include('application.libs.notifications.urls', namespace='notifications')),
    url(r'^blog/', include('application.apps.blog.urls', namespace='blog')),
    url(r'^invoice/', include('application.apps.invoice.urls', namespace='invoice')),
    url(r'^page/', include('application.apps.cms.urls', namespace='cms')),
    url(r'^contact/', include('application.apps.contact.urls', namespace='contact')),
    url(r'^faq/', include('application.apps.faq.urls', namespace='faq')),
    url(r'^deals/', include('application.apps.deals.urls', namespace='deals')),

    url(r'^edr/', include('application.apps.edr.urls', namespace='edr')),
    url(r'^interest/', include('application.apps.interest.urls', namespace='interest')),

    url(r'^ckeditor/', include('ckeditor.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'', include('debug_toolbar_user_panel.urls')),
   )
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        (r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),

        (r'^template/password_change_done/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/password_change_done.html'}),
        (r'^template/password_reset_complete/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/password_reset_complete.html'}),
        (r'^template/password_reset_confirm/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/password_reset_confirm.html'}),
        (r'^template/password_reset_done/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/password_reset_done.html'}),
        (r'^template/password_reset_email/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/password_reset_email.html'}),
    )

urlpatterns += patterns('',
        url(r'^', include('application.apps.ads.urls', namespace='ads')),
   )
