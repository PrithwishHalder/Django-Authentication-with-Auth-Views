from django.urls import path, include
from Accounts import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name="Homepage"),
    path('upload/', views.upload, name="upload"),
    path('signup/', views.signup, name='signup'),
    path('verify/<token>/', views.verify, name='VerifyUser'),
    path('login/', auth_view.LoginView.as_view(template_name="login.html", extra_context={'user': None}),
         name="Login"),
    path('logout/', auth_view.LogoutView.as_view(next_page="Homepage"),
         name="logoutUser"),
    path('change-password/', auth_view.PasswordChangeView.as_view(
        template_name='change_password.html', success_url='../logout/'), name='ChangePassword'),
    path('reset-password/', auth_view.PasswordResetView.as_view(template_name="forgotPass/resetPassword.html"),
         name="password_reset"),
    path('reset-password-sent/', auth_view.PasswordResetDoneView.as_view(template_name="forgotPass/ressetPasswordSent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(template_name="forgotPass/resetPasswordForm.html"), name="password_reset_confirm"),
    path('reset-password-done/',
         auth_view.PasswordResetCompleteView.as_view(template_name="forgotPass/resetPasswordDone.html"), name="password_reset_complete"),
]
