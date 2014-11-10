from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ImpostorageAppConfig(AppConfig):
    name = 'impostorage'
    verbose_name = _("Uploads")

    def ready(self):
        from .checks import settings_defined
        from .signals import file_deleted
        from .signals import file_saved
        from .listeners import handle_file_saved
        from .listeners import handle_file_deleted

        file_saved.connect(receiver=handle_file_saved,
                           dispatch_uid="impostorage_file_saved")
        file_deleted.connect(receiver=handle_file_deleted,
                             dispatch_uid="impostorage_file_deleted")
