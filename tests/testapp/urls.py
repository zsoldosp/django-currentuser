import django
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

from .models import TestModelDefaultBehavior, TestModelOnUpdate


if django.VERSION < (2, 0):
    from django.conf.urls import url as path
else:
    from django.urls import path


def create(request):
    if request.method == 'POST':
        TestModelDefaultBehavior.objects.create()
        return HttpResponse()


urlpatterns = [
    path(r'login/', auth_views.LoginView.as_view(), name="login"),
    path(r'create/', create, name="create"),
]
