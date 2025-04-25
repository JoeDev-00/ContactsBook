from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from contacts.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée des groupes par défaut pour tous les utilisateurs existants'

    def handle(self, *args, **options):
        users = User.objects.all()
        default_groups = [
            "Famille",
            "Amis",
            "Travail",
            "Collègues",
            "Importants"
        ]
        
        for user in users:
            self.stdout.write(f"Traitement de l'utilisateur: {user.username}")
            for group_name in default_groups:
                # Vérifier si le groupe existe déjà pour cet utilisateur
                if not Group.objects.filter(name=group_name, user=user).exists():
                    Group.objects.create(name=group_name, user=user)
                    self.stdout.write(f"  - Groupe '{group_name}' créé")
                else:
                    self.stdout.write(f"  - Groupe '{group_name}' existe déjà")
        
        self.stdout.write(self.style.SUCCESS('Groupes par défaut créés avec succès!'))
