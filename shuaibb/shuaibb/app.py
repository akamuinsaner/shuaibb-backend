from django.apps import AppConfig

class ShuaibbConfig(AppConfig):
    name = 'shuaibb'

    def ready(self):
        import shuaibb.signals