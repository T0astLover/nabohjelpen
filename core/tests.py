from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

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


class KategoriCrudTests(TestCase):
	def setUp(self):
		self.staff_user = User.objects.create_user(
			username='adminbruker',
			email='admin@example.com',
			password='trygt-passord-123',
			is_staff=True,
		)
		self.regular_user = User.objects.create_user(
			username='vanligbruker',
			email='bruker@example.com',
			password='trygt-passord-123',
		)
		self.kategori = Kategori.objects.create(
			navn='Handling',
			beskrivelse='Hjelp med handling',
		)

	def test_create_kategori_succeeds_with_valid_data(self):
		self.client.force_login(self.staff_user)
		response = self.client.post(reverse('kategori_opprett'), data={
			'navn': 'Omsorg',
			'beskrivelse': 'Praktisk hjelp og støtte til sårbare personer',
		})

		self.assertRedirects(response, reverse('kategori_liste'))
		self.assertTrue(Kategori.objects.filter(navn='Omsorg').exists())

	def test_kategori_list_view_shows_existing_categories_to_staff(self):
		self.client.force_login(self.staff_user)
		response = self.client.get(reverse('kategori_liste'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.kategori.navn)

	def test_kategori_detail_view_shows_category_details_to_staff(self):
		self.client.force_login(self.staff_user)
		response = self.client.get(reverse('kategori_detalj', args=[self.kategori.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.kategori.navn)
		self.assertContains(response, self.kategori.beskrivelse)

	def test_kategori_update_view_changes_category(self):
		self.client.force_login(self.staff_user)
		response = self.client.post(reverse('kategori_rediger', args=[self.kategori.pk]), data={
			'navn': 'Oppfølging',
			'beskrivelse': 'Kategori for videre oppfølging og støtte',
		})

		self.assertRedirects(response, reverse('kategori_liste'))
		self.kategori.refresh_from_db()
		self.assertEqual(self.kategori.navn, 'Oppfølging')
		self.assertEqual(self.kategori.beskrivelse, 'Kategori for videre oppfølging og støtte')

	def test_kategori_delete_view_removes_category(self):
		self.client.force_login(self.staff_user)
		response = self.client.post(reverse('kategori_slett', args=[self.kategori.pk]))

		self.assertRedirects(response, reverse('kategori_liste'))
		self.assertFalse(Kategori.objects.filter(pk=self.kategori.pk).exists())

	def test_kategori_create_view_rejects_duplicate_name_case_insensitive(self):
		self.client.force_login(self.staff_user)
		response = self.client.post(reverse('kategori_opprett'), data={
			'navn': 'handling',
			'beskrivelse': 'Duplikat med ulik store/små bokstaver',
		})

		self.assertEqual(response.status_code, 200)
		self.assertIn('navn', response.context['form'].errors)
		self.assertIn(
			'Kategorinavnet finnes allerede. Velg et annet navn.',
			response.context['form'].errors['navn'],
		)
		self.assertEqual(Kategori.objects.filter(navn__iexact='handling').count(), 1)

	def test_kategori_create_view_rejects_short_name(self):
		self.client.force_login(self.staff_user)
		response = self.client.post(reverse('kategori_opprett'), data={
			'navn': 'ab',
			'beskrivelse': 'For kort navn skal ikke lagres',
		})

		self.assertEqual(response.status_code, 200)
		self.assertIn('navn', response.context['form'].errors)
		self.assertIn(
			'Kategorinavnet må være minst 3 tegn langt.',
			response.context['form'].errors['navn'],
		)
		self.assertFalse(Kategori.objects.filter(navn='ab').exists())

	def test_kategori_create_view_redirects_anonymous_users_to_login(self):
		response = self.client.get(reverse('kategori_opprett'))

		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('login'), response.url)
		self.assertIn(reverse('kategori_opprett'), response.url)

	def test_kategori_create_view_forbidden_for_non_staff_users(self):
		self.client.force_login(self.regular_user)
		response = self.client.get(reverse('kategori_opprett'))

		self.assertEqual(response.status_code, 403)
