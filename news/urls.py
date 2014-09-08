from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

from web_ui.views import HomeView, DetailView, LoginView, SimpleSearchView


admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'news.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^(?i)user/', include('user.urls', namespace='user')),
                       url(r'^comments', include('django.contrib.comments.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^detail/(?P<news_id>\d*)$', DetailView.as_view(), name='detail'),
                       url(r'^management/', include('scheduler_manager.urls'), name='management'),
                       url(r'^(?i)rest/', include('rest.urls', namespace='rest')),
                       url(r'^(?i)$', HomeView.as_view(), name='home'),
                       url(r'^login/', LoginView.as_view(), name='login'),
                       url(r'^(?i)search/simple$', SimpleSearchView.as_view(), name='simple_search'),
                       (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
                       (r'^sitemap\.txt$', TemplateView.as_view(template_name='sitemap.xml', content_type='text/plain')),

)
#
# if settings.DEBUG:
#     urlpatterns = urlpatterns + url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
#                                     {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})
