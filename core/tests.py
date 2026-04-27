from django.test import TestCase
from django.contrib.auth.models import User

from .forms import RegistreringForm, ProfilForm, OppdragForm, KategoriForm, NyhetForm
from .models import Kategori, Profil


class FormValidationTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='eksisterende',
			email='eksisterende@example.com',
			password='trygt-passord-123'
		)
		self.kategori = Kategori.objects.create(navn='Handling', beskrivelse='Hjelp med handling')
		self.profil = Profil.objects.get(user=self.user)

	def test_registrering_krever_unik_epost_case_insensitive(self):
		form = RegistreringForm(data={
			'username': 'nybruker',
			'first_name': 'Ola',
			'last_name': 'Nordmann',
			'email': 'EKSISTERENDE@example.com',
			'telefon': '41234567',
			'password1': 'SterktPassord123!',
			'password2': 'SterktPassord123!'
		})
		self.assertFalse(form.is_valid())
		self.assertIn('email', form.errors)

	def test_registrering_fornavn_og_etternavn_kan_ikke_vaere_like(self):
		form = RegistreringForm(data={
			'username': 'samme-navn',
			'first_name': 'Ola',
			'last_name': 'ola',
			'email': 'ola@example.com',
			'telefon': '41234567',
			'password1': 'SterktPassord123!',
			'password2': 'SterktPassord123!'
		})
		self.assertFalse(form.is_valid())
		self.assertIn('last_name', form.errors)

	def test_profil_form_mangler_krevde_felter(self):
		form = ProfilForm(instance=self.profil, data={
			'telefon': '',
			'kan_hjelpe_med': '',
			'allergier_hensyn': '',
			'tilgjengelighet': ''
		})
		self.assertFalse(form.is_valid())
		self.assertIn('telefon', form.errors)
		self.assertIn('kan_hjelpe_med', form.errors)
		self.assertIn('tilgjengelighet', form.errors)

	def test_oppdrag_form_validerer_feltkonsistens(self):
		form = OppdragForm(data={
			'tittel': 'Bergen',
			'beskrivelse': 'For kort tekst',
			'sted': 'Bergen',
			'status': 'fullfort',
			'kategori': self.kategori.pk
		})
		self.assertFalse(form.is_valid())
		self.assertIn('sted', form.errors)
		self.assertIn('beskrivelse', form.errors)

	def test_kategori_form_validerer_case_insensitive_unikhet(self):
		form = KategoriForm(data={'navn': 'handling', 'beskrivelse': 'Test'})
		self.assertFalse(form.is_valid())
		self.assertIn('navn', form.errors)

	def test_nyhet_form_krever_mer_enn_tittel_i_innhold(self):
		form = NyhetForm(data={
			'tittel': 'Kort melding',
			'innhold': 'kort melding'
		})
		self.assertFalse(form.is_valid())
		self.assertIn('innhold', form.errors)
