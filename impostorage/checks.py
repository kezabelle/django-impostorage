# -*- coding: utf-8 -*-
from django.core.checks import register
from django.core.checks import Error
from django.core.checks import Warning


@register('impostorage', 'settings')
def settings_defined(app_configs):
    from django.conf import settings
    errors = []
    try:
        x = settings.IMPOSTORAGE_BACKEND
        has_setting = True
    except AttributeError:
        has_setting = False

    using_storage = settings.DEFAULT_FILE_STORAGE == 'impostorage.storage.WrappingStorage'  # noqa
    if using_storage is True and has_setting is False:
        errors.append(Error(
            "You won't be able to use `impostorage` as your"
            " `DEFAULT_FILE_STORAGE` without setting "
            "`IMPOSTORAGE_BACKEND`",
            hint="provide the dotted path to your real storage backend",
            obj=__name__, id='impostorage.E1',
        ))
    elif using_storage is False and has_setting is False:
        errors.append(Warning(
            "You won't be able to use the `impostorage` app without setting "
            "`IMPOSTORAGE_BACKEND`",
            hint="provide the dotted path to your real storage backend",
            obj=__name__, id='impostorage.W1',
        ))
    return errors
