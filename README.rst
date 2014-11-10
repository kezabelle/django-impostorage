django-impostorage
==================

A storage backend which wraps a real storage backend (set by
``IMPOSTORAGE_BACKEND``) and uses signals on ``save`` and ``delete``
to create ``FileUpload`` model instances.
