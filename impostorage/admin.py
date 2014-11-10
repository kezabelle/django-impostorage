# -*- coding: utf-8 -*-
from django.contrib import admin
from impostorage.models import FileUpload


class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['filename', 'dirname', 'created']
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(FileUpload, FileUploadAdmin)
