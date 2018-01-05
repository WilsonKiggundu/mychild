# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myChild.settings")
# os.environ["DJANGO_SETTINGS_MODULE"] = "myChild.settings"
# django.setup()

from django.apps import AppConfig
from django.contrib.auth.models import User

from api.models import SchoolEvent


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from actstream import registry
        # registry.register(self.get_model(SchoolEvent))
        # registry.register(self.get_model(User))
