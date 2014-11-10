# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.utils.deconstruct import deconstructible
from django.utils.encoding import python_2_unicode_compatible
from .signals import file_deleted
from .signals import file_saved


def get_underlying_storage():
    if not hasattr(settings, 'IMPOSTORAGE_BACKEND'):
        raise ImproperlyConfigured("To use `impostorage` as your file storage "
                                   "backend, you must set "
                                   "`IMPOSTORAGE_BACKEND` to the dotted path "
                                   "to the real storage backend you use.")
    return get_storage_class(import_path=settings.IMPOSTORAGE_BACKEND)


@deconstructible
@python_2_unicode_compatible
class WrappingStorage(object):
    def __init__(self):
        klass = get_underlying_storage()
        self.backend = klass()

    def __repr__(self):
        mod = self.__module__
        name = self.__class__.__name__
        backend_mod = self.backend.__module__
        backend_name = self.backend.__class__.__name__
        return '<{mod}.{name}: <{bmod}.{bname}>>'.format(mod=mod, name=name,
                                                         bmod=backend_mod,
                                                         bname=backend_name)

    def __str__(self):
        name = self.__class__.__name__
        backend_name = self.backend.__class__.__name__
        return '{name} wrapping over {bname}'.format(name=name,
                                                     bname=backend_name)

    def save(self, name, content):
        result = self.backend.save(name=name, content=content)
        file_saved.send(sender=self.backend.__class__, backend=self.backend,
                        filename=name, data=content, returned=result)
        return result

    def delete(self, name):
        result = self.backend.delete(name=name)
        file_deleted.send(sender=self.backend.__class__, backend=self.backend,
                          filename=name, returned=result)
        return result

    def open(self, *args, **kwargs):
        return self.backend.open(*args, **kwargs)

    def get_valid_name(self, *args, **kwargs):
        return self.backend.get_valid_name(*args, **kwargs)

    def get_available_name(self, *args, **kwargs):
        return self.backend.get_available_name(*args, **kwargs)

    def path(self, *args, **kwargs):
        return self.backend.path(*args, **kwargs)

    def exists(self, *args, **kwargs):
        return self.backend.exists(*args, **kwargs)

    def listdir(self, *args, **kwargs):
        return self.backend.listdir(*args, **kwargs)

    def size(self, *args, **kwargs):
        return self.backend.size(*args, **kwargs)

    def url(self, *args, **kwargs):
        return self.backend.url(*args, **kwargs)

    def accessed_time(self, *args, **kwargs):
        return self.backend.accessed_time(*args, **kwargs)

    def created_time(self, *args, **kwargs):
        return self.backend.created_time(*args, **kwargs)

    def modified_time(self, *args, **kwargs):
        return self.backend.modified_time(*args, **kwargs)
