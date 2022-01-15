from re import template
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('register', views.register_user, name='register_user'),
    path('edit', views.edit_user, name='edit_user'),
    path('change_passoword', views.ChangePasswordView.as_view(template_name='users/change-password.html'), name='change_password'),
    path('change_passoword_success', views.change_passoword_success, name='change_passoword_success'),
]