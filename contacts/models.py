from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date

def validate_phone_number(value):
    if not value.strip():
        raise ValidationError(_('Le numéro de téléphone est obligatoire.'))

def validate_name(value):
    return value and value.strip() != ""

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom du groupe")
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='contact_groups' 
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"
        ordering = ['name']
        unique_together = ['name', 'user']

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contacts")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Nom")
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Adresse")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    notes = models.TextField(blank=True, verbose_name="Notes")
    is_favorite = models.BooleanField(default=False, verbose_name="Favori")
    groups = models.ManyToManyField(Group, blank=True, related_name="contacts", verbose_name="Groupes")
    is_deleted = models.BooleanField(default=False, verbose_name="Supprimé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.phone_number

    def clean(self):
        if not validate_name(self.first_name) and not validate_name(self.last_name):
            raise ValidationError(_('Le prénom ou le nom doit être renseigné.'))

    def days_until_birthday(self):
        if not self.birth_date:
            return None
        
        today = date.today()
        next_birthday = date(today.year, self.birth_date.month, self.birth_date.day)
        
        if next_birthday < today:
            next_birthday = date(today.year + 1, self.birth_date.month, self.birth_date.day)
        
        return (next_birthday - today).days

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['last_name', 'first_name']
