from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from feedback.models import Forms, TextBox, MultiLine, CheckBox, MCQ, Option
from feedback.views.decorators import feedbackuser_login_required


@feedbackuser_login_required
def formfill(request, form_id):
    try:
        form = Forms.objects.get(pk=form_id)
    except KeyError:
        return HttpResponseRedirect(reverse("feedback_feedbackuser_formlist"))
    form_item_list = form.getInputs()
    context = {
        'item_list': form_item_list,
        'form_name': form.form_name
    }
    return render(request, 'feedback/feedbackuser_formfill.html', context)


