from feedback.models import Forms
from feedback.views.decorators import feedbackuser_login_required


@feedbackuser_login_required
def formfill(request, form_id):
    form = Forms.objects.get()