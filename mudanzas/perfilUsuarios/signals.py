from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Perfil
from registroUsuarios.models import Usuario

@receiver(post_save, sender=Usuario)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
