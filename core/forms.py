from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profil, Oppdrag, Kategori, Nyhet
import re


class AccessibleFormMixin:
    """Legger til konsekvente tilgjengelighetsattributter på alle felt."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            help_id = f"id_{field_name}_help"
            error_id = f"id_{field_name}_error"
            existing_describedby = field.widget.attrs.get('aria-describedby', '').strip()
            describedby_parts = [existing_describedby] if existing_describedby else []
            if field.help_text:
                describedby_parts.append(help_id)
            describedby_parts.append(error_id)
            field.widget.attrs['aria-describedby'] = ' '.join(describedby_parts)

            if field.required:
                field.widget.attrs['aria-required'] = 'true'


class RegistreringForm(AccessibleFormMixin, UserCreationForm):
    """Register new user"""
    username = forms.CharField(
        label=_('Brukernavn'),
        max_length=150,
        required=True,
        help_text=_('Velg et unikt brukernavn.'),
        error_messages={
            'required': _('Du må skrive inn et brukernavn.')
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Velg brukernavn')
        })
    )
    first_name = forms.CharField(
        label=_('Fornavn'),
        max_length=150,
        required=True,
        error_messages={
            'required': _('Du må skrive inn fornavn.')
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Fornavn')
        })
    )
    last_name = forms.CharField(
        label=_('Etternavn'),
        max_length=150,
        required=True,
        error_messages={
            'required': _('Du må skrive inn etternavn.')
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Etternavn')
        })
    )
    email = forms.EmailField(
        label=_('E-post'),
        required=True,
        error_messages={
            'required': _('Du må skrive inn en e-postadresse.'),
            'invalid': _('Skriv inn en gyldig e-postadresse, for eksempel navn@epost.no.')
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('din@epost.no')
        })
    )
    telefon = forms.CharField(
        label=_('Telefonnummer'),
        max_length=20,
        required=True,
        help_text=_('Skriv inn norsk telefonnummer.'),
        error_messages={
            'required': _('Du må skrive inn telefonnummer.')
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('+47 XX XX XX XX')
        })
    )
    password1 = forms.CharField(
        label=_('Passord'),
        error_messages={
            'required': _('Du må skrive inn et passord.')
        },
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label=_('Bekreft passord'),
        error_messages={
            'required': _('Du må bekrefte passordet.')
        },
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefon', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        first_name = (cleaned_data.get('first_name') or '').strip().lower()
        last_name = (cleaned_data.get('last_name') or '').strip().lower()

        if first_name and last_name and first_name == last_name:
            self.add_error('last_name', _('Fornavn og etternavn kan ikke være like.'))

        return cleaned_data

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('Denne e-postadressen er allerede registrert.'))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Dette brukernavnet er allerede tatt.'))
        if len(username) < 3:
            raise forms.ValidationError(_('Brukernavnet må være minst 3 tegn langt.'))
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name.strip()) < 2:
            raise forms.ValidationError(_('Fornavn må være minst 2 tegn langt.'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name.strip()) < 2:
            raise forms.ValidationError(_('Etternavn må være minst 2 tegn langt.'))
        return last_name

    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon', '').strip()
        telefon_renset = telefon.replace(' ', '')

        if not re.fullmatch(r'(\+47)?\d{8}', telefon_renset):
            raise forms.ValidationError(
                _('Telefonnummeret må være et gyldig norsk nummer med 8 sifre. Eksempel: 41234567 eller +4741234567.')
            )

        return telefon_renset


class ProfilForm(AccessibleFormMixin, forms.ModelForm):
    """Edit profile"""
    class Meta:
        model = Profil
        fields = ('telefon', 'kan_hjelpe_med', 'allergier_hensyn', 'tilgjengelighet')
        widgets = {
            'telefon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Telefonnummer')
            }),
            'kan_hjelpe_med': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Hva kan du hjelpe til med?')
            }),
            'allergier_hensyn': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Allergier eller spesielle hensyn')
            }),
            'tilgjengelighet': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Når er du tilgjengelig?')
            }),
        }
        error_messages = {
            'telefon': {
                'required': _('Du må skrive inn telefonnummer.')
            },
            'kan_hjelpe_med': {
                'required': _('Du må beskrive hva du kan hjelpe med.')
            },
            'tilgjengelighet': {
                'required': _('Du må skrive når du er tilgjengelig.')
            },
        }
        help_texts = {
            'telefon': _('Skriv inn norsk telefonnummer med 8 sifre.'),
            'kan_hjelpe_med': _('Skriv kort hva slags oppgaver du kan hjelpe med.'),
            'allergier_hensyn': _('Fyll inn dersom det er noe organisasjonen bør ta hensyn til.'),
            'tilgjengelighet': _('Eksempel: hverdager etter kl. 16 eller helger.')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefon'].required = True
        self.fields['kan_hjelpe_med'].required = True
        self.fields['tilgjengelighet'].required = True

    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon', '').strip()
        telefon_renset = telefon.replace(' ', '')

        if not re.fullmatch(r'(\+47)?\d{8}', telefon_renset):
            raise forms.ValidationError(
                _('Telefonnummeret må være et gyldig norsk nummer med 8 sifre. Eksempel: 41234567 eller +4741234567.')
            )

        return telefon_renset

    def clean(self):
        cleaned_data = super().clean()
        kan_hjelpe_med = (cleaned_data.get('kan_hjelpe_med') or '').strip()
        tilgjengelighet = (cleaned_data.get('tilgjengelighet') or '').strip()

        if kan_hjelpe_med and tilgjengelighet and kan_hjelpe_med.lower() == tilgjengelighet.lower():
            self.add_error(
                'tilgjengelighet',
                _('Tilgjengelighet kan ikke være lik teksten i "Hva kan du hjelpe med". Beskriv når du faktisk kan bidra.')
            )

        return cleaned_data


class OppdragForm(AccessibleFormMixin, forms.ModelForm):
    """Create/edit assignment"""
    class Meta:
        model = Oppdrag
        fields = ('tittel', 'beskrivelse', 'sted', 'status', 'kategori')
        widgets = {
            'tittel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Tittel på oppdraget')
            }),
            'beskrivelse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Beskriv oppdraget')
            }),
            'sted': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Sted')
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'tittel': {
                'required': _('Du må skrive inn en tittel på oppdraget.')
            },
            'beskrivelse': {
                'required': _('Du må skrive inn en beskrivelse av oppdraget.')
            },
            'sted': {
                'required': _('Du må skrive inn sted for oppdraget.')
            },
            'kategori': {
                'required': _('Du må velge en kategori.')
            },
            'status': {
                'required': _('Du må velge en status.')
            },
        }
        help_texts = {
            'tittel': _('Velg en kort og tydelig tittel.'),
            'beskrivelse': _('Forklar hva oppdraget går ut på, slik at frivillige forstår det.'),
            'sted': _('Skriv tydelig sted, for eksempel gateadresse eller møtested.'),
            'status': _('Velg status som passer den nåværende situasjonen for oppdraget.')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.fields['status'].initial = 'aapen'

    def clean_tittel(self):
        tittel = self.cleaned_data.get('tittel', '').strip()
        if len(tittel) < 5:
            raise forms.ValidationError(_('Tittelen må være minst 5 tegn lang.'))
        return tittel

    def clean_beskrivelse(self):
        beskrivelse = self.cleaned_data.get('beskrivelse', '').strip()
        if len(beskrivelse) < 10:
            raise forms.ValidationError(_('Beskrivelsen må være minst 10 tegn lang.'))
        return beskrivelse

    def clean_sted(self):
        sted = self.cleaned_data.get('sted', '').strip()
        if len(sted) < 2:
            raise forms.ValidationError(_('Sted må være minst 2 tegn langt.'))
        return sted

    def clean(self):
        cleaned_data = super().clean()
        tittel = (cleaned_data.get('tittel') or '').strip().lower()
        sted = (cleaned_data.get('sted') or '').strip().lower()
        status = cleaned_data.get('status')
        beskrivelse = (cleaned_data.get('beskrivelse') or '').strip()

        if tittel and sted and tittel == sted:
            self.add_error('sted', _('Sted kan ikke være identisk med tittelen. Skriv hvor oppdraget skal utføres.'))

        if status == 'fullfort' and len(beskrivelse) < 30:
            self.add_error(
                'beskrivelse',
                _('Når et oppdrag er markert som fullført, må beskrivelsen være minst 30 tegn og forklare resultatet.')
            )

        return cleaned_data


class KategoriForm(AccessibleFormMixin, forms.ModelForm):
    """Create/edit category"""
    class Meta:
        model = Kategori
        fields = ('navn', 'beskrivelse')
        widgets = {
            'navn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Kategorinavn')
            }),
            'beskrivelse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Beskrivelse')
            }),
        }
        error_messages = {
            'navn': {
                'required': _('Du må skrive inn navn på kategorien.')
            },
        }
        help_texts = {
            'navn': _('Velg et kort navn som beskriver typen oppdrag.'),
            'beskrivelse': _('Valgfritt: utdyp hva kategorien brukes til.')
        }

    def clean_navn(self):
        navn = self.cleaned_data.get('navn', '').strip()
        if len(navn) < 3:
            raise forms.ValidationError(_('Kategorinavnet må være minst 3 tegn langt.'))

        eksisterende = Kategori.objects.filter(navn__iexact=navn)
        if self.instance.pk:
            eksisterende = eksisterende.exclude(pk=self.instance.pk)
        if eksisterende.exists():
            raise forms.ValidationError(_('Kategorinavnet finnes allerede. Velg et annet navn.'))

        return navn


class NyhetForm(AccessibleFormMixin, forms.ModelForm):
    """Create/edit news"""
    class Meta:
        model = Nyhet
        fields = ('tittel', 'innhold')
        widgets = {
            'tittel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Tittel')
            }),
            'innhold': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Innhold')
            }),
        }
        error_messages = {
            'tittel': {
                'required': _('Du må skrive inn en tittel.')
            },
            'innhold': {
                'required': _('Du må skrive inn innhold i nyheten.')
            },
        }
        help_texts = {
            'tittel': _('Lag en konkret overskrift som gjør det lett å forstå nyheten.'),
            'innhold': _('Skriv tydelig informasjon. Unngå svært korte meldinger.')
        }

    def clean_tittel(self):
        tittel = self.cleaned_data.get('tittel', '').strip()
        if len(tittel) < 5:
            raise forms.ValidationError(_('Tittelen må være minst 5 tegn lang.'))
        return tittel

    def clean_innhold(self):
        innhold = self.cleaned_data.get('innhold', '').strip()
        if len(innhold) < 20:
            raise forms.ValidationError(_('Innholdet må være minst 20 tegn langt.'))
        return innhold

    def clean(self):
        cleaned_data = super().clean()
        tittel = (cleaned_data.get('tittel') or '').strip().lower()
        innhold = (cleaned_data.get('innhold') or '').strip().lower()

        if tittel and innhold and tittel == innhold:
            self.add_error('innhold', _('Innholdet kan ikke være identisk med tittelen. Legg til mer forklarende informasjon.'))

        return cleaned_data