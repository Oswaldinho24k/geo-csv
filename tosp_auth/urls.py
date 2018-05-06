from django.conf.urls import url

from . import views

app_name = 'tosp_auth'

urlpatterns = [
    url(r'^login/$',
        views.TospAuthLoginView.as_view(),
        name='login'),
    url(r'^logout/$',
        views.TospAuthLogoutView.as_view(),
        name='logout'),
    url(r'^password_change/$',
        views.TospAuthPasswordChangeView.as_view(),
        name='password_change'),
    url(r'^password_change/done/$',
        views.TospAuthPasswordChangeDoneView.as_view(),
        name='password_change_done'),
    url(r'^password_reset/$',
        views.TospAuthPasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password_reset/done/$',
        views.TospAuthPasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.TospAuthPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^reset/done/$',
        views.TospAuthPasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
