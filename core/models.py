from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone


class Kategori(models.Model):
    """Kategori for oppdrag"""
    navn = models.CharField(max_length=100, unique=True)
    beskrivelse = models.TextField(blank=True)
    opprettet = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Kategorier"
        ordering = ['navn']

    def __str__(self):
        return self.navn


class Profil(models.Model):
    """Frivilligs profil"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    telefon = models.CharField(max_length=20, blank=True)
    kan_hjelpe_med = models.TextField(
        blank=True,
        help_text="Hva kan du hjelpe til med?"
    )
    allergier_hensyn = models.TextField(
        blank=True,
        help_text="Allergier eller spesielle hensyn"
    )
    tilgjengelighet = models.TextField(
        blank=True,
        help_text="Når er du tilgjengelig?"
    )
    opprettet = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Profiler"
        ordering = ['-opprettet']

    def __str__(self):
        return f"Profil for {self.user.get_full_name() or self.user.username}"


class Oppdrag(models.Model):
    """Oppdrag/aktivitet som frivillige kan melde seg på"""
    
    STATUS_CHOICES = (
        ('aapen', 'Åpen'),
        ('paagaar', 'Pågår'),
        ('fullfort', 'Fullført'),
    )

    tittel = models.CharField(max_length=200)
    beskrivelse = models.TextField()
    sted = models.CharField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aapen')
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, related_name='oppdrag')
    opprettet_av = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opprettede_oppdrag')
    opprettet = models.DateTimeField(auto_now_add=True)
    pameldte = models.ManyToManyField(User, related_name='pameldte_oppdrag', blank=True)

    class Meta:
        verbose_name_plural = "Oppdrag"
        ordering = ['-opprettet']

    def __str__(self):
        return self.tittel

    def antall_pameldte(self):
        return self.pameldte.count()


class Nyhet(models.Model):
    """Nyheter og informasjon"""
    tittel = models.CharField(max_length=300)
    innhold = models.TextField()
    opprettet_av = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opprettede_nyheter')
    publisert_dato = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Nyheter"
        ordering = ['-publisert_dato']

    def __str__(self):
        return self.tittel
