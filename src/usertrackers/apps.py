from django.apps import AppConfig


class UsertrackersConfig(AppConfig):
    name = 'usertrackers'

    def ready(self):
        import usertrackers.signals
