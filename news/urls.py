from django.conf.urls import patterns, include, url

from django.contrib import admin
from web_ui.views import HomeView

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'news.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^(?i)$', HomeView.as_view(), name='home'),

)
