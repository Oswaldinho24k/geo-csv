from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy


class TospAuthLoginView(auth_views.LoginView):
    template_name = 'tosp_auth/login.html'


class TospAuthLogoutView(auth_views.LogoutView):
    template_name = 'tosp_auth/logged_out.html'


class TospAuthPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'tosp_auth/password_change.html'
    success_url = reverse_lazy('tosp_auth:password_change_done')


class TospAuthPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'tosp_auth/password_change_done.html'


class TospAuthPasswordResetView(auth_views.PasswordResetView):
    template_name = 'tosp_auth/password_reset_form.html'
    email_template_name = 'tosp_auth/password_reset_email.html'
    success_url = reverse_lazy('tosp_auth:password_reset_done')


class TospAuthPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'tosp_auth/password_reset_done.html'


class TospAuthPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'tosp_auth/password_reset_confirm.html'
    success_url = reverse_lazy('tosp_auth:password_reset_complete')


class TospAuthPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'tosp_auth/password_reset_complete.html'
