from django.http import HttpResponse
from django.shortcuts import render
from feedback.constants import *


# Create your views here.
def index(request):
    context = {}
    try:
        error = request.GET['error']
    except KeyError:
        return render(request, 'feedback/login.html')
    if error == "pass":
        context['error_msg'] = PASSWORD_ERROR_MESSAGE
    elif error == "user":
        context['error_msg'] = USERNAME_ERROR_MESSAGE
    render(request, 'feedback/login.html', context)


