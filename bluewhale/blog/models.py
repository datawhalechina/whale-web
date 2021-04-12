from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from core.models import User


class Article(models.Model):
    class Status(models.IntegerChoices):
        normal = 0
        deleted = 1
        blocked = 2

    id = models.CharField(_('id'), primary_key=True, max_length=36)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(_('title'), max_length=64, blank=False)
    content = models.TextField(_('content'), blank=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modified at'), auto_now=True)
    status = models.IntegerField(_('status'), choices=Status.choices, default=Status.normal)