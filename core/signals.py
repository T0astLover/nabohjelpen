from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profil


@receiver(post_save, sender=User)
def opprett_profil(sender, instance, created, **kwargs):
    """Opprett automatisk profil når ny bruker blir opprettet"""
    if created:
        Profil.objects.create(user=instance)


@receiver(post_save, sender=User)
def lagre_profil(sender, instance, **kwargs):
    """Lagre profil når bruker blir lagret"""
    if hasattr(instance, 'profil'):
        instance.profil.save()
