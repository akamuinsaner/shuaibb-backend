from django.apps import AppConfig

class ShuaibbConfig(AppConfig):
    name = 'shuaibb'

    def ready(self):
        import shuaibb.signals
        # todo 增加自动 migrate
        from django.db.migrations.migration import *

