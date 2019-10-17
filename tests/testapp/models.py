from django.db import models
from django_currentuser.db.models import CurrentUserField


class TestModelOnUpdate(models.Model):
    updated_by = CurrentUserField(on_update=True)


class TestModelDefaultBehavior(models.Model):
    created_by = CurrentUserField()
