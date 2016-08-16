from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from feedback.exceptions import UserAuthenticationFailedException


def login_admin(request):
    try:
        error = request.GET['error']
        context = {'error_message': 'Login Failed'}
    except KeyError:
        context = {}
    return render(request, 'feedback/admin/login.html', context)


def authenticate_admin(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise UserAuthenticationFailedException
    except (KeyError, UserAuthenticationFailedException):
        return HttpResponseRedirect(reverse('admin_login') + "?error=true")

    login(request, user)
