# -*- coding: utf-8 -*-
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from .storage import get_underlying_storage
from model_utils.models import TimeStampedModel
import os


class FileUpload(TimeStampedModel):
    filename = CharField(max_length=255, null=False, blank=False)
    dirname = CharField(max_length=255, null=True, blank=False)

    def realpath(self):
        if self.dirname:
            return os.path.join(self.dirname, self.filename)
        return self.filename

    def get_absolute_url(self):
        # maybe something like this ...
        return get_underlying_storage()().url(self.realpath())

    class Meta:
        verbose_name = _("file upload")
        verbose_name_plural = _("file uploads")
