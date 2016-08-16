from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from feedback.models import FeedbackUser, Forms, Survey


def formlist(request):
    try:
        username = request.POST['username']
    except KeyError:
        return HttpResponseRedirect(reverse('feedback_index') + "?error=user")
    try:
        user = FeedbackUser.objects.get(user_name=username)
    except FeedbackUser.DoesNotExist:
        return HttpResponseRedirect(reverse('feedback_index') + "?error=user")
    form_list = Forms.objects.all().filter(user=user,
                                           finished=False,
                                           survey__in=Survey.objects.all().filter(finished=False))
    return render(request, 'feedback/feedbackuser_formlist', context={
        'form_list': form_list
    })
