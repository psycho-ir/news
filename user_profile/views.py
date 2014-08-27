from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _


@login_required(login_url='/user/login')
class ChangePasswordView():
    def get(self, request, error_message=None, message=None):
        pass

    def post(self, request):
        oldPass = request.POST["oldPass"]
        newPass = request.POST["newPass"]

        if request.user.check_password(oldPass):
            request.user.set_password(newPass)
            request.user.save()
            context = RequestContext(request, {'message': _('password has been changed')})

            return self.get()
        else:
            return HttpResponse("!!!!!")







