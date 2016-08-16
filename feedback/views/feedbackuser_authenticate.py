from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from feedback.models import FeedbackUser


def authenticate(request):
    try:
        username = request.POST['username']
    except KeyError:
        return HttpResponseRedirect(reverse('feedback_index') + "?error=user")
    try:
        user = FeedbackUser.objects.get(user_name=username)
    except FeedbackUser.DoesNotExist:
        return HttpResponseRedirect(reverse('feedback_index') + "?error=user")
    request.session['user'] = user
    return HttpResponseRedirect(reverse('feedback_feedbackuser_formlist'))
