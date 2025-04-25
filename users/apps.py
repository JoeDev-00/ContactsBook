from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

def ready(self):
    import users.signals # Importer le module signals pour s'assurer que les signaux sont enregistrés