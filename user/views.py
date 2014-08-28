from functools import wraps
import logging

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.views.generic import View

from Postchi.Mail import send_confirm_mail
from Postchi.models import ConfirmMail
from news import settings
from user.login import auth_user


errorLogger = logging.getLogger('error')


def is_user_anon(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return HttpResponseRedirect(settings.DEFAULT_LOGIN_URL)
            else:
                return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@is_user_anon(login_url=settings.DEFAULT_LOGIN_URL)
def user_login(request):
    if request.method == "POST":
        return auth_user(request)

    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponse("You have been authenticated before!")
        template = loader.get_template('login.html')
        context = RequestContext(request)
        return HttpResponse(template.render(context))

    render_to_response
    return HttpResponse("Wrong Method!")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(settings.DEFAULT_LOGOUT_URL)


@is_user_anon(login_url=settings.DEFAULT_LOGIN_URL)
def user_register(request):
    register_template = loader.get_template('register.html')

    if request.method == "POST":
        name = request.POST["name"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        username = request.POST["email"]
        password = request.POST["password"]
        password_again = request.POST["password_again"]
        if password != password_again:
            context = RequestContext(request, {'error_message': "Password confirmation is wrong"})
            return HttpResponse(register_template.render(context))


        is_exist = User.objects.filter(email=email).count() > 0
        u = User(username=username, first_name=name, last_name=last_name, email=email)
        u.set_password(password)
        try:
            if is_exist:
                raise ValidationError("")
            u.full_clean()
        except ValidationError as e:
            if is_exist:
                context = RequestContext(request, {'error_message': "You have been registered with this email"})
            else:
                context = RequestContext(request, {'validation_error': e})
            return HttpResponse(register_template.render(context))
        u.is_active = False
        u.save()

        from Postchi.Mail import send_confirm_mail
        send_confirm_mail(u)  # Send Confirmation Link

        return HttpResponseRedirect(reverse('user:pending'))
    else:
        context = RequestContext(request)
        return HttpResponse(register_template.render(context))


@is_user_anon(login_url=settings.DEFAULT_LOGIN_URL)
def show_pending(request):
    pending_template = loader.get_template('pending_for_confirm.html')
    context = RequestContext(request)
    return HttpResponse(pending_template.render(context))


def confirm(request, user_id, confirm_code):
    try:
        user = User.objects.get(id=user_id)
        is_valid = is_confim_valid(user_id, confirm_code)
        if is_valid:
            user.is_active = True
            user.save()
            template = loader.get_template('confirm.html')
            context = RequestContext(request)
            return HttpResponse(template.render(context))

        else:
            return HttpResponse("confirm code is wrong")

    except ObjectDoesNotExist as e:
        logging.info('Error: ' + e.message)
        return HttpResponse("User does not exist")


def confirm_again(request):
    if request.method == "POST":
        try:
            email = request.POST["email"]
            user = User.objects.get(email=email.strip())
            ConfirmMail.objects.filter(user_id=user.id).delete()
            send_confirm_mail(user)
            return HttpResponseRedirect(reverse('user:pending'))
        except Exception as e:
            print e
            return HttpResponseRedirect(reverse('home'))
    else:

        template = loader.get_template('confirm_again.html')
        context = RequestContext(request)
        return HttpResponse(template.render(context))


def is_confim_valid(user_id, confirm_code):
    try:
        # confirmation = ConfirmMail.objects.get(confirm_key=confirm_code, user_id=user_id)
        return True
    except ObjectDoesNotExist as e:
        logging.info('Error: ' + e.message)
        return False


class ChangePasswordView(View):
    def get(self, request, error_message=None, message=None):
        return render_to_response('change_pass.html', {'error_message': error_message, 'message': message}, RequestContext(request))

    def post(self, request):
        oldPass = request.POST["currentPass"]
        newPass = request.POST["newPass"]

        if request.user.check_password(oldPass):
            request.user.set_password(newPass)
            request.user.save()

            return self.get(request, message='Password has been changed')
        else:
            return self.get(request, error_message='Error in changing password')

