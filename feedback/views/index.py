from django.http import HttpResponse
from django.shortcuts import render
from feedback.constants import *


# Create your views here.
def index(request):
    context = {}
    try:
        error = request.GET['error']
    except KeyError:
        return render(request, 'feedback/index.html')
    if error == "pass":
        context['error_msg'] = PASSWORD_ERROR_MESSAGE
    render(request, 'feedback/index.html', context)


