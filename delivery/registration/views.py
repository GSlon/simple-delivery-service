import logging
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignInForm, SignUpForm
from .services.dbservice import check_user_exists_from_form, try_register_user, authorize_user
from .services.dbservice import get_user_id_from_form


logger = logging.getLogger(__name__)


def default_path_redirect(request):
    return HttpResponseRedirect('signin')


def sign_in(request):
    if request.method == 'GET':
        form = SignInForm()
        return render(request, 'registration/signin.html', {'form': form})
    elif request.method == 'POST':
        signinform = SignInForm(request.POST)
        if signinform.is_valid():
            if check_user_exists_from_form(signinform):
                if authorize_user(signinform):
                    id = get_user_id_from_form(signinform)
                    return HttpResponseRedirect('map/{0}'.format(id))
                else:
                    return HttpResponse('invalid password')
            else:
                return HttpResponseRedirect('signup')
        else:
            return HttpResponse('Invalid data')


def sign_up(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
    elif request.method == 'POST':
        signupform = SignUpForm(request.POST)
        if signupform.is_valid():
            if try_register_user(signupform):
                return HttpResponseRedirect('signin')
            else:
                return HttpResponse('user exists')
        else:
            return HttpResponse('Invalid data')
