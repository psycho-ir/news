from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from user import views
from user.views import ChangePasswordView


__author__ = 'soroosh'

urlpatterns = patterns('',
                       url(r'^(?i)login$', views.user_login, name='login'),
                       url(r'^(?i)logout$', views.user_logout, name='logout'),
                       url(r'^(?i)register$', views.user_register, name='register'),
                       url(r'^(?i)pending', views.show_pending, name='pending'),
                       url(r'^(?i)reconfirm', views.confirm_again, name='confirm_again'),
                       url(r'^(?i)change_pass', login_required(ChangePasswordView.as_view(),login_url='/'), name='change_pass'),
                       url(r'^(?i)confirm/(?P<user_id>\d*)-(?P<confirm_code>\w*)$', views.confirm, name='confirm'),
)
