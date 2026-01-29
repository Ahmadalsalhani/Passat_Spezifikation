from django.contrib import admin
from .models import Kunde, Raumtyp, Raum, Buchung, Belegungsprotokoll, Rechnung, Rechnungsposten


@admin.register(Kunde)
class KundeAdmin(admin.ModelAdmin):
    list_display = ['vorname', 'nachname', 'email', 'telefonnummer', 'ort', 'erstellt_am']
    search_fields = ['vorname', 'nachname', 'email', 'telefonnummer']
    list_filter = ['land', 'datenschutz_akzeptiert', 'erstellt_am']
    readonly_fields = ['erstellt_am', 'aktualisiert_am']


@admin.register(Raumtyp)
class RaumtypAdmin(admin.ModelAdmin):
    list_display = ['name', 'typ', 'preis_pro_nacht']
    list_filter = ['typ']


@admin.register(Raum)
class RaumAdmin(admin.ModelAdmin):
    list_display = ['nummer', 'name', 'raumtyp', 'kapazitaet', 'ist_aktiv']
    list_filter = ['ist_aktiv', 'raumtyp']
    search_fields = ['nummer', 'name']


class BelegungsprotokollInline(admin.TabularInline):
    model = Belegungsprotokoll
    extra = 1


@admin.register(Buchung)
class BuchungAdmin(admin.ModelAdmin):
    list_display = ['buchungsnummer', 'kunde', 'raum', 'anreise_datum', 'abreise_datum', 'status', 'erstellt_am']
    list_filter = ['status', 'anreise_datum', 'erstellt_am']
    search_fields = ['buchungsnummer', 'kunde__vorname', 'kunde__nachname', 'raum__nummer']
    readonly_fields = ['buchungsnummer', 'erstellt_am', 'aktualisiert_am', 'anzahl_naechte']
    inlines = [BelegungsprotokollInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.erstellt_von = request.user
        super().save_model(request, obj, form, change)


@admin.register(Belegungsprotokoll)
class BelegungsprotokollAdmin(admin.ModelAdmin):
    list_display = ['buchung', 'leistung', 'datum', 'anzahl', 'einzelpreis', 'gesamtbetrag']
    list_filter = ['datum']
    search_fields = ['leistung', 'buchung__buchungsnummer']
    readonly_fields = ['gesamtbetrag']


class RechnungspostenInline(admin.TabularInline):
    model = Rechnungsposten
    extra = 1


@admin.register(Rechnung)
class RechnungAdmin(admin.ModelAdmin):
    list_display = ['rechnungsnummer', 'buchung', 'rechnungsdatum', 'faelligkeitsdatum', 'gesamtbetrag', 'status']
    list_filter = ['status', 'rechnungsdatum']
    search_fields = ['rechnungsnummer', 'buchung__buchungsnummer', 'buchung__kunde__nachname']
    readonly_fields = ['rechnungsnummer', 'erstellt_am', 'aktualisiert_am']
    inlines = [RechnungspostenInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.erstellt_von = request.user
        super().save_model(request, obj, form, change)


@admin.register(Rechnungsposten)
class RechnungspostenAdmin(admin.ModelAdmin):
    list_display = ['rechnung', 'beschreibung', 'menge', 'einzelpreis', 'gesamtpreis']
    search_fields = ['beschreibung', 'rechnung__rechnungsnummer']
    readonly_fields = ['gesamtpreis']
