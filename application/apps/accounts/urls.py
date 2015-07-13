from django.conf.urls import patterns, url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^switch_business_profile/(?P<business_profile_id>\d+)/$', views.switch_business_profile, name="switch_profile"),
    url(r'^test/has_active_business_profile$', views.test_view),
    url(r'^change_language/(?P<lang_code>\w+)/$', views.change_language, name="change_language"),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^details/$', views.AccountFormView.as_view(), name='account_form'),

    url(r'^$', login_required(views.MyAccountListView.as_view()), name='index'),
    url(r'^(?P<group>ads|deals)/(?P<type>\w+)/$', login_required(views.MyAccountListView.as_view()), name='index'),

    url(r'^agent/$', views.AgentDashboard.as_view(), name='agent_index'),
)
