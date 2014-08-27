__author__ = 'soroosh'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from scheduler_manager.views import *


urlpatterns = patterns('',
                       url(r'^(?i)', login_required(ManagementHomeView.as_view()), name='home'),
                       # url(r'^(?i)logout$', views.user_logout, name='logout'),
                       # url(r'^(?i)register$', views.user_register, name='register'),
                       # url(r'^(?i)pending', views.show_pending, name='pending'),
                       # url(r'^(?i)reconfirm', views.confirm_again, name='confirm_again'),
                       # url(r'^(?i)change_pass', login_required(ChangePasswordView.as_view(),login_url='/'), name='change_pass'),
                       # url(r'^(?i)confirm/(?P<user_id>\d*)-(?P<confirm_code>\w*)$', views.confirm, name='confirm'),
)
