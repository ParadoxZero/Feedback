from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from feedback.models import Survey


def index(request):
    try:
        msg = request.GET['msg']
        context = {'error_message': 'Some error has occured'}
        # TODO include messages for add success, close success and errors
    except KeyError:
        context = {}
    return render(request, 'feedback/admin/survey_home.html', context)


def add_survey(request):
    try:
        error = request.GET['error']
        context = {"erro_message": 'Some error has occured'} # TODO error message to constant
    except KeyError:
        context = {}
    return render(request, 'feedback/admin/survey_add.html', context)


def add_survey_validate(request):
    try:
        survey_name = request.POST['survey_name']
    except KeyError:
        return HttpResponseRedirect(reverse('admin_survey_add')+"?error=true")
    s = Survey()
    s.name = survey_name
    s.date_created = timezone.now()
    s.save()
    return HttpResponseRedirect(reverse('admin_survey_index')+"?msg=add")


def close_survey(request):
    try:
        error = request.GET['error']
        context = {"error_message": "Some error has occured"} # TODO specify error message to constant
    except KeyError:
        context = {}
    s = Survey.objects.filter(finished=False)
    context['survey_list'] = s
    return render(request, 'feedback/admin/survey_close.html', context)


def close_survey_validate(request):
    try:
        s = request.POST['survey']
    except KeyError:
        return HttpResponseRedirect(reverse("admin_survey_close")+"?error=true")
    s = Survey.objects.get(pk=s)
    s.finished = True
    s.save()
    return HttpResponseRedirect(reverse("admin_survey_index"))


def edit_survey(request):
    try:
        error = request.GET['error']
        context = {'error_message': 'some error has occured'} # TODO error message
    except KeyError:
        context = {}
    s = Survey.objects.all()
    context['survey_list'] = s
    return render(request, 'feedback/admin/survey_edit.html', context)


def edit_survey_validate(request):
    try:
        s = int(request.POST['survey'])
        name = request.POST['name']
        delete = request.POST['delete']
    except KeyError:
        return HttpResponseRedirect(reverse('admin_survey_edit')+"?error=error")
    if bool(delete):
        Survey.objects.get(pk=s).delete()
    else:
        Survey.objects.get(pk=s).name = name
    return HttpResponseRedirect(reverse('admin_survey_index'))