from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def feedbackuser_login_required(func):
    def wrapper_func(request):
        try:
            user = request.session['user']
        except KeyError:
            return HttpResponseRedirect(reverse('feedback_index') + "?error=user")
        return func(request)

    return wrapper_func
