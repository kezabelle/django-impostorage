# -*- coding: utf-8 -*-
import logging
from .models import FileUpload
import os


logger = logging.getLogger(__name__)


def handle_file_saved(sender, backend, filename, data, returned, **kwargs):
    dirname, fname = os.path.split(filename)
    if not dirname:
        dirname = None
    if not fname:
        logger.error("Couldn't save the appropriate FileUpload because "
                     "the resulting filename part was empty.")
    return FileUpload.objects.get_or_create(filename=fname, dirname=dirname)


def handle_file_deleted(sender, backend, filename, returned, **kwargs):
    dirname, fname = os.path.split(filename)
    if not dirname:
        dirname = None
    if not fname:
        logger.error("Couldn't delete the appropriate FileUpload because "
                     "the resulting filename part was empty.")
        return None
    return FileUpload.objects.filter(filename=fname, dirname=dirname).delete()
