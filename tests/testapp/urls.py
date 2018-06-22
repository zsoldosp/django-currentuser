import django
from django.contrib.auth import views as auth_views


if django.VERSION < (2, 0):
    from django.conf.urls import url as path
else:
    from django.urls import path


urlpatterns = [
    path(r'login/', auth_views.LoginView.as_view(), name="login")
]
