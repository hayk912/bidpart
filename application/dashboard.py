"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'bidpart-django.dashboard.CustomIndexDashboard'
"""
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import DashboardModule
from grappelli.dashboard.utils import get_admin_site_name


class RecentActions(DashboardModule):
    """
    Module that lists the recent actions for the all users.
    """

    title = _('Recent Actions')
    template = 'grappelli/dashboard/modules/recent_actions.html'
    limit = 10
    include_list = None
    exclude_list = None

    def __init__(self, title=None, limit=10, include_list=None,
                 exclude_list=None, **kwargs):
        self.include_list = include_list or []
        self.exclude_list = exclude_list or []
        kwargs.update({'limit': limit})
        super(RecentActions, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        if self._initialized:
            return
        from django.db.models import Q
        from django.contrib.admin.models import LogEntry

        request = context['request']

        def get_qset(list):
            qset = None
            for contenttype in list:
                if isinstance(contenttype, ContentType):
                    current_qset = Q(content_type__id=contenttype.id)
                else:
                    try:
                        app_label, model = contenttype.split('.')
                    except:
                        raise ValueError('Invalid contenttype: "%s"' % contenttype)
                    current_qset = Q(
                        content_type__app_label=app_label,
                        content_type__model=model
                    )
                if qset is None:
                    qset = current_qset
                else:
                    qset = qset | current_qset
            return qset

        qs = LogEntry.objects.all()

        if self.include_list:
            qs = qs.filter(get_qset(self.include_list))
        if self.exclude_list:
            qs = qs.exclude(get_qset(self.exclude_list))

        self.children = qs.select_related('content_type', 'user')[:self.limit]
        self._initialized = True


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = 'Bidpart Administration'

        # Users and groups
        self.children.append(modules.AppList(
            _('Users & Businesses'),
            collapsible=True,
            column=1,
            css_classes=('collapse grp-closed',),
            models=('django.contrib.auth.*', 'application.apps.accounts.*', 'application.apps.interest.*'),
        ))

        # Ads and deals
        self.children.append(modules.AppList(
            _('Ads & Deals'),
            column=1,
            css_classes=('collapse grp-closed',),
            models=('application.apps.ads.*', 'application.apps.deals.*', 'application.apps.invoice.models.*'),
            exclude=('application.apps.invoice.models.InvoiceLogEntry', 'application.apps.ads.models.Value')
        ))

        # Site Content
        self.children.append(modules.AppList(
            _('Site content'),
            column=1,
            css_classes=('collapse grp-closed',),
            models=('application.apps.cms.*', 'application.apps.blog.*', 'application.apps.faq.*'),
        ))

        # Files & Images
        self.children.append(modules.ModelList(
            _('Files & Images'),
            column=1,
            css_classes=('collapse grp-closed',),
            models=('application.apps.files.*', ),
        ))

        # Files & Images
        self.children.append(modules.ModelList(
            _('Settings'),
            column=1,
            css_classes=('collapse grp-closed',),
            models=('application.apps.adminsettings.*', 'currencies.*'),
        ))

        # Logs
        self.children.append(modules.ModelList(
            _('Admin logs'),
            column=1,
            css_classes=('collapse grp-closed',),
            models=('django.contrib.admin.models.LogEntry', ),
        ))

        # append a recent actions module
        self.children.append(RecentActions(
            _('All Recent Actions'),
            limit=10,
            collapsible=False,
            column=2,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Your Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


