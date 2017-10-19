import sys
import warnings

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user


class CurrentUserField(models.ForeignKey):

    warning = ("You passed an argument to CurrentUserField that will be "
               "ignored. Avoid args and following kwargs: default, null, to.")
    description = _(
        'as default value sets the current logged in user if available')

    def __init__(self, *a, **kw):
        test_arg = sys.argv[2:3]
        is_test_run = test_arg and 'test' in test_arg.pop()
        if (a or set(kw).intersection({"default", "null", "to"})) and not is_test_run:
            warnings.warn(self.warning)
        if "on_delete" not in kw:
            kw["on_delete"] = models.CASCADE
        kw.update(dict(null=True, default=get_current_authenticated_user,
                       to="auth.User"))
        super(CurrentUserField, self).__init__(**kw)
