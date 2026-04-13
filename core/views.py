from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.translation import gettext as _
from .models import Oppdrag, Profil, Nyhet, Kategori
from .forms import (
    RegistreringForm, ProfilForm, OppdragForm, NyhetForm, KategoriForm
)


# ============== AUTENTISERING ==============

class ForsidenView(TemplateView):
    """Forside med oversikt"""
    template_name = 'forsiden.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['antall_medlemmer'] = User.objects.filter(is_staff=False).count()
        context['aapne_oppdrag_count'] = Oppdrag.objects.filter(status='aapen').count()
        context['fullforte_oppdrag_count'] = Oppdrag.objects.filter(status='fullfort').count()
        context['nyeste_oppdrag'] = Oppdrag.objects.filter(status='aapen')[:3]
        context['nyeste_nyheter'] = Nyhet.objects.all()[:3]
        return context


class RegistreringView(CreateView):
    """Registrering av ny bruker"""
    model = User
    form_class = RegistreringForm
    template_name = 'registrering.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Lagre bruker
        response = super().form_valid(form)
        # Hent telefon fra form data
        telefon = form.cleaned_data.get('telefon', '')
        # Oppdater profilen med telefon
        user = self.object
        user.profil.telefon = telefon
        user.profil.save()
        messages.success(self.request, _('Bruker opprettet! Logg inn med dine detaljer.'))
        return response


class ProsjektLoginView(LoginView):
    """Login"""
    template_name = 'login.html'
    redirect_authenticated_user = True


class ProsjektLogoutView(LogoutView):
    """Logout"""
    next_page = reverse_lazy('forsiden')


# ============== BRUKER-DASHBOARD ==============

class DashboardView(LoginRequiredMixin, TemplateView):
    """Bruker dashboard"""
    template_name = 'dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bruker_profil'] = self.request.user.profil
        context['pameldte_oppdrag'] = self.request.user.pameldte_oppdrag.all()
        return context


# ============== PROFIL-VIEWS ==============

class ProfilDetailView(LoginRequiredMixin, DetailView):
    """Vis brukers profil"""
    model = Profil
    template_name = 'profil_detalj.html'
    context_object_name = 'profil'
    login_url = 'login'

    def get_object(self):
        return self.request.user.profil


class ProfilUpdateView(LoginRequiredMixin, UpdateView):
    """Rediger brukers profil"""
    model = Profil
    form_class = ProfilForm
    template_name = 'profil_rediger.html'
    success_url = reverse_lazy('profil_detalj')
    login_url = 'login'

    def get_object(self):
        return self.request.user.profil

    def form_valid(self, form):
        messages.success(self.request, _('Profil oppdatert!'))
        return super().form_valid(form)


class SlettKontoView(LoginRequiredMixin, DeleteView):
    """Slett brukerkontoView"""
    model = User
    template_name = 'slett_konto.html'
    success_url = reverse_lazy('forsiden')
    login_url = 'login'

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Kontoen din er slettet.'))
        return super().delete(request, *args, **kwargs)


# ============== OPPDRAG-VIEWS ==============

class OppdragListView(ListView):
    """Liste over alle oppdrag"""
    model = Oppdrag
    template_name = 'oppdrag_liste.html'
    context_object_name = 'oppdrag'
    paginate_by = 5

    def get_queryset(self):
        qs = Oppdrag.objects.select_related('kategori', 'opprettet_av').all().order_by('-opprettet')
        
        # Filter på status
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(status=status)
        
        # Filter på kategori
        kategori = self.request.GET.get('kategori', '')
        if kategori:
            qs = qs.filter(kategori__id=kategori)
        
        # Søk
        search = self.request.GET.get('search', '')
        if search:
            qs = qs.filter(
                Q(tittel__icontains=search) | Q(beskrivelse__icontains=search)
            )
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategorier'] = Kategori.objects.all()
        context['status_choices'] = Oppdrag.STATUS_CHOICES
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['querystring'] = query_params.urlencode()
        return context


class OppdragDetailView(DetailView):
    """Detalj om oppdrag"""
    model = Oppdrag
    template_name = 'oppdrag_detalj.html'
    context_object_name = 'oppdrag'

    def get_queryset(self):
        return Oppdrag.objects.select_related('kategori', 'opprettet_av').prefetch_related('pameldte')


class OppdragCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Opprett nytt oppdrag (admin)"""
    model = Oppdrag
    form_class = OppdragForm
    template_name = 'oppdrag_create.html'
    success_url = reverse_lazy('oppdrag_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.opprettet_av = self.request.user
        messages.success(self.request, _('Oppdrag opprettet!'))
        return super().form_valid(form)


class OppdragUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Rediger oppdrag (admin)"""
    model = Oppdrag
    form_class = OppdragForm
    template_name = 'oppdrag_update.html'
    success_url = reverse_lazy('oppdrag_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.get_object().opprettet_av == self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Oppdrag oppdatert!'))
        return super().form_valid(form)


class OppdragDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Slett oppdrag (admin)"""
    model = Oppdrag
    template_name = 'oppdrag_delete.html'
    success_url = reverse_lazy('oppdrag_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Oppdrag slettet!'))
        return super().delete(request, *args, **kwargs)


class PameldingView(LoginRequiredMixin, View):
    """Meld deg på oppdrag"""
    login_url = 'login'

    def post(self, request, pk):
        oppdrag = get_object_or_404(Oppdrag, pk=pk)
        if request.user not in oppdrag.pameldte.all():
            oppdrag.pameldte.add(request.user)
            messages.success(request, _('Du er nå påmeldt "%(title)s"!') % {'title': oppdrag.tittel})
        else:
            messages.info(request, _('Du er allerede påmeldt dette oppdraget.'))
        return redirect('oppdrag_detalj', pk=pk)


class AvmeldingView(LoginRequiredMixin, View):
    """Meld deg av oppdrag"""
    login_url = 'login'

    def post(self, request, pk):
        oppdrag = get_object_or_404(Oppdrag, pk=pk)
        if request.user in oppdrag.pameldte.all():
            oppdrag.pameldte.remove(request.user)
            messages.success(request, _('Du er nå avmeldt "%(title)s".') % {'title': oppdrag.tittel})
        return redirect('oppdrag_detalj', pk=pk)


# ============== NYHETER-VIEWS ==============

class NyhetListView(ListView):
    """Liste over nyheter"""
    model = Nyhet
    template_name = 'nyhet_liste.html'
    context_object_name = 'nyheter'
    paginate_by = 5

    def get_queryset(self):
        qs = Nyhet.objects.select_related('opprettet_av').all().order_by('-publisert_dato')

        search = self.request.GET.get('search', '')
        if search:
            qs = qs.filter(
                Q(tittel__icontains=search) | Q(innhold__icontains=search)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['querystring'] = query_params.urlencode()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class NyhetDetailView(DetailView):
    """Detalj om nyhet"""
    model = Nyhet
    template_name = 'nyhet_detalj.html'
    context_object_name = 'nyhet'


class NyhetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Opprett nyhet (admin)"""
    model = Nyhet
    form_class = NyhetForm
    template_name = 'nyhet_create.html'
    success_url = reverse_lazy('nyhet_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.opprettet_av = self.request.user
        messages.success(self.request, _('Nyhet publisert!'))
        return super().form_valid(form)


class NyhetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Rediger nyhet (admin)"""
    model = Nyhet
    form_class = NyhetForm
    template_name = 'nyhet_update.html'
    success_url = reverse_lazy('nyhet_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.get_object().opprettet_av == self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Nyhet oppdatert!'))
        return super().form_valid(form)


class NyhetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Slett nyhet (admin)"""
    model = Nyhet
    template_name = 'nyhet_delete.html'
    success_url = reverse_lazy('nyhet_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Nyhet slettet!'))
        return super().delete(request, *args, **kwargs)


# ============== KATEGORI-VIEWS ==============

class KategoriListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Liste over kategorier (admin)"""
    model = Kategori
    template_name = 'kategori_liste.html'
    context_object_name = 'kategorier'
    paginate_by = 5
    login_url = 'login'

    def get_queryset(self):
        qs = Kategori.objects.all().order_by('navn')

        search = self.request.GET.get('search', '')
        if search:
            qs = qs.filter(
                Q(navn__icontains=search) | Q(beskrivelse__icontains=search)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['querystring'] = query_params.urlencode()
        context['search_query'] = self.request.GET.get('search', '')
        return context

    def test_func(self):
        return self.request.user.is_staff


class KategoriDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Detalj om kategori"""
    model = Kategori
    template_name = 'kategori_detalj.html'
    context_object_name = 'kategori'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Kategori.objects.prefetch_related('oppdrag__opprettet_av')


class KategoriCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Opprett kategori (admin)"""
    model = Kategori
    form_class = KategoriForm
    template_name = 'kategori_create.html'
    success_url = reverse_lazy('kategori_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, _('Kategori opprettet!'))
        return super().form_valid(form)


class KategoriUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Rediger kategori (admin)"""
    model = Kategori
    form_class = KategoriForm
    template_name = 'kategori_update.html'
    success_url = reverse_lazy('kategori_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, _('Kategori oppdatert!'))
        return super().form_valid(form)


class KategoriDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Slett kategori (admin)"""
    model = Kategori
    template_name = 'kategori_delete.html'
    success_url = reverse_lazy('kategori_liste')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Kategori slettet!'))
        return super().delete(request, *args, **kwargs)
