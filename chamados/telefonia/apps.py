from django.apps import AppConfig


class TelefoniaConfig(AppConfig):
    name = 'chamados.telefonia'
    verbose_name = "Telefonia"

    def ready(self):
        pass