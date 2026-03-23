from django.contrib import admin
from .models import Profil, Kategori, Oppdrag, Nyhet


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('get_bruker_navn', 'telefon', 'opprettet')
    search_fields = ('user__first_name', 'user__last_name', 'telefon')
    readonly_fields = ('opprettet',)

    def get_bruker_navn(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_bruker_navn.short_description = 'Bruker'


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('navn', 'opprettet')
    search_fields = ('navn',)
    ordering = ('navn',)


@admin.register(Oppdrag)
class OppdragAdmin(admin.ModelAdmin):
    list_display = ('tittel', 'kategori', 'status', 'get_opprettet_av', 'antall_pameldte', 'opprettet')
    list_filter = ('status', 'kategori', 'opprettet')
    search_fields = ('tittel', 'beskrivelse', 'sted')
    readonly_fields = ('opprettet', 'opprettet_av')
    filter_horizontal = ('pameldte',)

    def get_opprettet_av(self, obj):
        return obj.opprettet_av.get_full_name() or obj.opprettet_av.username
    get_opprettet_av.short_description = 'Opprettet av'

    def save_model(self, request, obj, form, change):
        if not change:  # Nytt objekt
            obj.opprettet_av = request.user
        super().save_model(request, obj, form, change)


@admin.register(Nyhet)
class NyhetAdmin(admin.ModelAdmin):
    list_display = ('tittel', 'get_opprettet_av', 'publisert_dato')
    list_filter = ('publisert_dato',)
    search_fields = ('tittel', 'innhold')
    readonly_fields = ('opprettet_av', 'publisert_dato')

    def get_opprettet_av(self, obj):
        return obj.opprettet_av.get_full_name() or obj.opprettet_av.username
    get_opprettet_av.short_description = 'Opprettet av'

    def save_model(self, request, obj, form, change):
        if not change:  # Nytt objekt
            obj.opprettet_av = request.user
        super().save_model(request, obj, form, change)
