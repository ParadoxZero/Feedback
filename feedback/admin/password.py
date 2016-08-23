from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    try:
        error = request.GET['error']
        context = {'error_message': 'some error has occured'}  # TODO error message
    except KeyError:
        context = {}

    return render(request, 'feedback/admin/password.html', context)


def validate(request):
    try:
        username = request.POST['username']
        old_password = request.POST['old']
        new_password = request.POST['new']
        new_password_again = request.POST['new_again']
    except KeyError:
        return HttpResponseRedirect(reverse('admin_password_index') + "?error=error")  # TODO set better error code

    user = authenticate(username=username, password=old_password)
    if user is None:
        return HttpResponseRedirect(reverse('admin_password_index') + "?error=error")
    if new_password != new_password_again:
        return HttpResponseRedirect(reverse('admin_password_index') + "?error=error")
    user.set_password(new_password)
    return HttpResponseRedirect(reverse('admin_password_index'))
