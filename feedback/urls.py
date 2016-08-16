from django.conf.urls import url

from feedback import views
from feedback.views import index, feedbackuser_authenticate, feedbackuser_formlist, feedbackuser_formfill
from feedback.views import feedbackuser_form_validate

'''
Naming convention :
variables  - small letters - underscore eg test_run
class - camel case , starting with capital eg TestRun
name - camel case with small letter start eg testRun
'''

urlpatterns =[
    url(r'^$', views.index.index, name="feedback_index"),
    url(r'student/$', views.feedbackuser_authenticate.authenticate, name="feedback_feedbackuser_authenticate"),
    url(r'student/form/$', views.feedbackuser_formlist.formlist, name="feedback_feedbackuser_formlist'"),
    url(r'student/form/fill/(?P<form_id>[0-9]+)$', views.feedbackuser_formfill.formfill,
        name="feedback_feedbackuser_formfill"),
    url(r'student/form/fill/verify/$', views.feedbackuser_form_validate.validate,
        name="feedback_feedbackuser_validate"),

]
