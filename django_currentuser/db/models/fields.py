from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user


class CurrentUserField(models.ForeignKey):
    description = _(
        'as default value sets the current logged in user if available')

    def __init__(self, *a, **kw):
        kw.update(dict(null=True, default=get_current_authenticated_user,
                       to="auth.User"))
        super(CurrentUserField, self).__init__(**kw)
