# -*- coding: utf-8 -*-
import django.dispatch

file_saved = django.dispatch.Signal(providing_args=[
    "backend", "filename", "data", "returned"
])

file_deleted = django.dispatch.Signal(providing_args=[
    "backend", "filename", "returned"
])
