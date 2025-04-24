import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Répertoire.settings')

application = get_wsgi_application()

# Ajout pour Vercel
app = application
