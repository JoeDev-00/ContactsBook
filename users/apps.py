from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

def ready(self):
    import users.signals  # Importer les signaux ici pour s'assurer qu'ils sont chargés
