from django.apps import AppConfig


class PerfilusuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perfilUsuarios'
    
    def ready(self):
        import perfilUsuarios.signals