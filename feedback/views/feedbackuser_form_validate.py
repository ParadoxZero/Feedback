from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from feedback.models import Forms, Option
from feedback.views.decorators import feedbackuser_login_required


@feedbackuser_login_required
def validate(request):
    try:
        form_id = request.POST['form_id']
    except KeyError:
        return HttpResponseRedirect(reverse("feedback_feedbackuser_formlist"))
    try:
        form = Forms.objects.get(pk=form_id)
        form_items_list = form.getInputs()
        for item in form_items_list:
            value = request.POST[str(item.position)]
            if item[0] == 'tb' or item[0] == 'mb':
                item[1].data = value
            elif item[0] == 'cb':
                item[1].data = bool(value)
            else:
                option = Option.objects.get(pk=value)
                option.data = True
                option.save()
            item[1].save()
    except KeyError:
        return HttpResponseRedirect(reverse("feedback_feedbackuser_formfill"), args=form_id)
    return HttpResponseRedirect(reverse("feedback_feedbackuser_formlist"))

