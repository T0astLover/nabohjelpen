# 🏘️ Nabohjelpen - Norsk Frivillighetsplattform

En komplett Django-applikasjon for en norsk frivillighetsplattform som kobler sammen naboer som ønsker å hjelpe hverandre.

## Teknologi

- **Django 6.0** - Web framework
- **SQLite** - Database
- **Python 3.10+** - Programming language
- **Django Auth System** - Brukerautentisering
- **Class-based Views** - CreateView, ListView, DetailView, UpdateView, DeleteView
- **ModelForms** - Skjemahåndtering
- **Django Signals** - Automatisk profil-opprettelse

## Prosjektstruktur

```
nabohjelpen/
├── manage.py                 # Django management
├── db.sqlite3               # SQLite database
├── config/                  # Django config
│   ├── settings.py         # Innstillinger
│   ├── urls.py             # Hovedelleruter
│   ├── wsgi.py             # WSGI config
│   └── asgi.py             # ASGI config
├── core/                    # Hovedapp
│   ├── models.py           # Modeller (Profil, Oppdrag, Nyhet, Kategori)
│   ├── views.py            # Class-based views
│   ├── forms.py            # ModelForms
│   ├── urls.py             # App-ruter
│   ├── admin.py            # Admin panel config
│   ├── signals.py          # Signaler (auto profil)
│   ├── migrations/         # Database migrations
│   └── apps.py             # App config
└── templates/              # HTML templates
    ├── base.html           # Basis template
    ├── forsiden.html       # Homepage
    ├── registrering.html   # Registration
    ├── login.html          # Login
    ├── dashboard.html      # User dashboard
    ├── profil_*.html       # Profil templates
    ├── oppdrag_*.html      # Oppdrag templates
    ├── nyhet_*.html        # Nyhet templates
    └── kategori_*.html     # Kategori templates
```

## Modeller

### **Profil** (OneToOne med User)
- `user` - Link til Django User
- `telefon` - Telefonnummer
- `kan_hjelpe_med` - Hvilke oppgaver man kan hjelpe med
- `allergier_hensyn` - Allergier og spesielle hensyn
- `tilgjengelighet` - Når man er tilgjengelig
- `opprettet` - Tidspunkt

### **Kategori**
- `navn` - Kategorinavn (unik)
- `beskrivelse` - Beskrivelse av kategori
- `opprettet` - Tidspunkt

### **Oppdrag**
- `tittel` - Oppdragets tittel
- `beskrivelse` - Detaljert beskrivelse
- `sted` - Hvor oppdraget skal gjøres
- `status` - Åpen / Pågår / Fullført
- `kategori` - ForeignKey til Kategori
- `opprettet_av` - Bruker som opprettet oppdraget
- `opprettet` - Tidspunkt
- `pameldte` - ManyToMany med User (frivillige som er påmeldt)

### **Nyhet**
- `tittel` - Nyhetstitel
- `innhold` - Full tekst
- `opprettet_av` - Bruker som skrev det
- `publisert_dato` - Publikasjonsdato

## Funksjonalitet

### 🔐 Autentisering
- ✅ Brukerregistrering med valideringer
- ✅ Login og logout
- ✅ Automatisk profil-opprettelse via Django signals
- ✅ Passordbeskyttelse

### 👤 Dashboard & Profil
- ✅ Bruker dashboard med oversikt
- ✅ Rediger egen profil
- ✅ Se påmeldte oppdrag
- ✅ Slett konto (permanent)

### 📋 Oppdrag
- ✅ Liste over alle oppdrag
- ✅ Søk og filter (status, kategori, tittel)
- ✅ Se detaljer om oppdrag
- ✅ Meld deg på oppdraget
- ✅ Trekk deg fra (avmelding)
- ✅ Admin: Opprett/rediger/slett oppdrag

### 📰 Nyheter
- ✅ Liste over nyheter
- ✅ Se full nyhet
- ✅ Admin: Publiser/rediger/slett nyheter

### 📂 Kategorier
- ✅ Admin: Full CRUD for kategorier
- ✅ Brukt for filtrering av oppdrag

### 📊 Forside
- ✅ Medlemsteller (viser antall frivillige)
- ✅ 3 siste oppdrag
- ✅ 3 siste nyheter
- ✅ Call-to-action for registrering

### 🔒 Sikkerhet
- ✅ LoginRequiredMixin for beschyttede sider
- ✅ UserPassesTestMixin for admin-funksjoner
- ✅ CSRF-beskyttelse
- ✅ Passordvali

## Installasjon & Kjøring

### 1. Klone eller åpne prosjektet
```bash
cd c:\Users\nikol\Downloads\nabohjelpen
```

### 2. Opprett virtual environment (hvis ikke allerede gjort)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installer Django
```bash
pip install django
```

### 4. Kjør migrasjoner
```bash
python manage.py migrate
```

### 5. Opprett superbruker (admin)
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (velg passord)
```

### 6. Start development server
```bash
python manage.py runserver
```

**Server kjører på:** `http://localhost:8000`

### 7. Logg inn på admin panel
```
http://localhost:8000/admin/
```

## Bruki for første gang

### Opprette startdata:

1. **Opprett kategorier på admin**
   - Gå til `/admin`
   - Opprett kategorier som "Handle", "Kjøring", "Hagearbeid", etc.

2. **Opprett testoppdrag**
   - Opprett noen oppdrag (må være logget inn som admin)
   - Fyll inn tittel, beskrivelse, sted, og velg kategori

3. **Registrer deg som bruker**
   - Gå til `/registrering/`
   - Opprett ny bruker
   - Logg inn på dashboard

4. **Meld deg på oppdrag**
   - Gå til `/oppdrag/`
   - Klikk på et oppdrag
   - Klikk "Meld deg på"

5. **Publiser nyheter**
   - Som admin, gå til `/nyheter/opprett/`
   - Skriv og publiser nyhet

## URLs (Ruter)

### Offentlige
- `/` - Forside
- `/registrering/` - Registrering
- `/login/` - Login
- `/oppdrag/` - Liste over oppdrag
- `/oppdrag/<id>/` - Detaljer om oppdrag
- `/nyheter/` - Liste over nyheter
- `/nyheter/<id>/` - Lesing av nyhet

### Kun innlogget
- `/dashboard/` - Bruker dashboard
- `/profil/` - Min profil
- `/profil/rediger/` - Rediger profil
- `/profil/slett/` - Slett konto
- `/oppdrag/<id>/pameld/` - Meld deg på
- `/oppdrag/<id>/avmeld/` - Avmeld deg

### Kun admin
- `/admin/` - Django admin panel
- `/oppdrag/opprett/` - Opprett oppdrag
- `/oppdrag/<id>/rediger/` - Rediger oppdrag
- `/oppdrag/<id>/slett/` - Slett oppdrag
- `/nyheter/opprett/` - Publiser nyhet
- `/nyheter/<id>/rediger/` - Rediger nyhet
- `/nyheter/<id>/slett/` - Slett nyhet
- `/kategorier/` - Liste kategorier
- `/kategorier/opprett/` - Opprett kategori
- `/kategorier/<id>/rediger/` - Rediger kategori
- `/kategorier/<id>/slett/` - Slett kategori

## Styling

Prosjektet bruker inline CSS i base.html for enkelt og ryddig design. Alt er responsivt og fungerer på mobile enheter.

**Farger:**
- Primær (blå): `#3498db`
- Suksess (grønn): `#27ae60`
- Fare (rød): `#e74c3c`
- Bakgrunn: `#f5f5f5`

## Språk

Alt er på **Norsk Bokmål** (nb), inkludert:
- UI tekst
- Feltlabels
- Meldinger
- Stringsannotasjoner

## Feilsøking

### "ModuleNotFoundError: No module named 'django'"
```bash
pip install django
```

### Database feil
```bash
python manage.py migrate
python manage.py migrate core
```

### Superbruker glemt
Du kan opprette ny superbruker:
```bash
python manage.py createsuperuser
```

### Templates ikke funnet
Sjekk at `TEMPLATES['DIRS']` i settings.py inneholder `BASE_DIR / 'templates'`

## Testing

For å teste med testdata i admin:

1. Logg inn på `/admin`
2. Opprett 3-5 kategorier
3. Opprett 5-10 oppdrag under ulike kategorier
4. Opprett et par nyheter
5. Registrer deg som bruker og test funksjonalitet

## Produksjonsveileding

For å kjøre i produksjon, husk å:

1. Sett `DEBUG = False` i settings.py
2. Sett `SECRET_KEY` til tilfeldige verdier
3. Legg til `ALLOWED_HOSTS`
4. Bruk PostgreSQL i stedet for SQLite
5. Sett opp HTTPS
6. Bruk `.env` fil for sensitiv data

## Ressurser

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Class-based Views](https://docs.djangoproject.com/en/6.0/topics/class-based-views/)
- [Django Forms](https://docs.djangoproject.com/en/6.0/topics/forms/)

## Lisens

Privat skoleprojekt - alle koder eieredd av skolen/eleven.

---

**Laget med ❤️ for et velfungerende frivillighetssamfunn**
