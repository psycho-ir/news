from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest import views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'news.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^latest/', views.LatestNewsView.as_view(), name='latest'),
                       url(r'^like/', views.LikeView.as_view(), name='like'),
                       url(r'^bookmark/', views.BookmarkView.as_view(), name='bookmark'),

)
