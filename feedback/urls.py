from django.conf.urls import url, include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'.*', include('feedback.urls'))
]