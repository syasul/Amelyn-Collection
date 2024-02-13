from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User'

    def ready(self):
        # NOTE: Don't delete these below lines, it's for scheduled task
        # from scheduled import due_date_reminder
        # due_date_reminder.start()
        pass
