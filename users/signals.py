from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from contacts.models import Group

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_groups(sender, instance, created, **kwargs):
    """
    Crée des groupes par défaut pour chaque nouvel utilisateur
    """
    if created:
        default_groups = [
            "Famille",
            "Amis",
            "Travail",
            "Collègues",
            "Importants"
        ]
        
        for group_name in default_groups:
            Group.objects.create(name=group_name, user=instance)
