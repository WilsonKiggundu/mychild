from django.apps import AppConfig
from django.contrib.auth.models import User


class DefaultAppConfig(AppConfig):
    name = 'api'

    def ready(self):
        from actstream import registry
        registry.register(User, self.get_model('Profile'))
