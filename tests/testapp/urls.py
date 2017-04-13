from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = (
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^login/$', auth_views.login, name="login"),
)
