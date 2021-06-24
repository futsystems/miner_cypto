


from django.apps import AppConfig

class SignalsConfig(AppConfig):
    name = 'miner_chia'

    def ready(self):
        import server.signals.harvester_service_restart_handler