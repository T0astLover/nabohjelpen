from django.urls import path
from . import views

urlpatterns = [
    # Autentisering
    path('', views.ForsidenView.as_view(), name='forsiden'),
    path('registrering/', views.RegistreringView.as_view(), name='registrering'),
    path('login/', views.ProsjektLoginView.as_view(), name='login'),
    path('logout/', views.ProsjektLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Profil
    path('profil/', views.ProfilDetailView.as_view(), name='profil_detalj'),
    path('profil/rediger/', views.ProfilUpdateView.as_view(), name='profil_rediger'),
    path('profil/slett/', views.SlettKontoView.as_view(), name='slett_konto'),
    
    # Oppdrag
    path('oppdrag/', views.OppdragListView.as_view(), name='oppdrag_liste'),
    path('oppdrag/<int:pk>/', views.OppdragDetailView.as_view(), name='oppdrag_detalj'),
    path('oppdrag/opprett/', views.OppdragCreateView.as_view(), name='oppdrag_opprett'),
    path('oppdrag/<int:pk>/rediger/', views.OppdragUpdateView.as_view(), name='oppdrag_rediger'),
    path('oppdrag/<int:pk>/slett/', views.OppdragDeleteView.as_view(), name='oppdrag_slett'),
    path('oppdrag/<int:pk>/pameld/', views.PameldingView.as_view(), name='pameld'),
    path('oppdrag/<int:pk>/avmeld/', views.AvmeldingView.as_view(), name='avmeld'),
    
    # Nyheter
    path('nyheter/', views.NyhetListView.as_view(), name='nyhet_liste'),
    path('nyheter/<int:pk>/', views.NyhetDetailView.as_view(), name='nyhet_detalj'),
    path('nyheter/opprett/', views.NyhetCreateView.as_view(), name='nyhet_opprett'),
    path('nyheter/<int:pk>/rediger/', views.NyhetUpdateView.as_view(), name='nyhet_rediger'),
    path('nyheter/<int:pk>/slett/', views.NyhetDeleteView.as_view(), name='nyhet_slett'),
    
    # Kategorier
    path('kategorier/', views.KategoriListView.as_view(), name='kategori_liste'),
    path('kategorier/<int:pk>/', views.KategoriDetailView.as_view(), name='kategori_detalj'),
    path('kategorier/opprett/', views.KategoriCreateView.as_view(), name='kategori_opprett'),
    path('kategorier/<int:pk>/rediger/', views.KategoriUpdateView.as_view(), name='kategori_rediger'),
    path('kategorier/<int:pk>/slett/', views.KategoriDeleteView.as_view(), name='kategori_slett'),
]
