from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profil, Oppdrag, Kategori, Nyhet


class RegistreringForm(UserCreationForm):
    """Register new user"""
    username = forms.CharField(
        label=_('Brukernavn'),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Velg brukernavn')})
    )
    first_name = forms.CharField(
        label=_('Fornavn'),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Fornavn')})
    )
    last_name = forms.CharField(
        label=_('Etternavn'),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Etternavn')})
    )
    email = forms.EmailField(
        label=_('E-post'),
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('din@epost.no')})
    )
    telefon = forms.CharField(
        label=_('Telefonnummer'),
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('+47 XX XX XX XX')})
    )
    password1 = forms.CharField(
        label=_('Passord'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label=_('Bekreft passord'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefon', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Denne e-postadressen er allerede registrert.'))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Dette brukernavnet er allerede tatt.'))
        return username


class ProfilForm(forms.ModelForm):
    """Edit profile"""
    class Meta:
        model = Profil
        fields = ('telefon', 'kan_hjelpe_med', 'allergier_hensyn', 'tilgjengelighet')
        widgets = {
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Telefonnummer')}),
            'kan_hjelpe_med': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Hva kan du hjelpe til med?')}),
            'allergier_hensyn': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Allergier eller spesielle hensyn')}),
            'tilgjengelighet': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Når er du tilgjengelig?')}),
        }


class OppdragForm(forms.ModelForm):
    """Create/edit assignment"""
    class Meta:
        model = Oppdrag
        fields = ('tittel', 'beskrivelse', 'sted', 'status', 'kategori')
        widgets = {
            'tittel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Tittel på oppdraget')}),
            'beskrivelse': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('Beskriv oppdraget')}),
            'sted': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Sted')}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
        }


class KategoriForm(forms.ModelForm):
    """Create/edit category"""
    class Meta:
        model = Kategori
        fields = ('navn', 'beskrivelse')
        widgets = {
            'navn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Kategorinavn')}),
            'beskrivelse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Beskrivelse')}),
        }


class NyhetForm(forms.ModelForm):
    """Create/edit news"""
    class Meta:
        model = Nyhet
        fields = ('tittel', 'innhold')
        widgets = {
            'tittel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Tittel')}),
            'innhold': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('Innhold')}),
        }
