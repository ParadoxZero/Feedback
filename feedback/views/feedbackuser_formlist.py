from django.shortcuts import render

from feedback.models import Survey, Forms
from feedback.views.decorators import feedbackuser_login_required


@feedbackuser_login_required
def formlist(request):
    user = request.session['user']
    form_list = Forms.objects.all().filter(user=user,
                                           finished=False,
                                           survey__in=Survey.objects.all().filter(finished=False))
    return render(request, 'feedback/feedbackuser_formlist.html', context={
        'form_list': form_list
    })
