from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import View

from scheduler import simple_scheduler


class ManagementHomeView(View):
    def get(self, request):
        schedulers = simple_scheduler.__registry__
        return render_to_response('management_home.html', {'schedulers': schedulers}, RequestContext(request))

