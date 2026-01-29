from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


class Kunde(models.Model):
    """Customer model - Kundenverwaltung"""
    vorname = models.CharField(max_length=100, verbose_name="Vorname")
    nachname = models.CharField(max_length=100, verbose_name="Nachname")
    email = models.EmailField(verbose_name="E-Mail")
    telefon_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefonnummer muss im Format eingegeben werden: '+999999999'. Bis zu 15 Ziffern erlaubt."
    )
    telefonnummer = models.CharField(
        validators=[telefon_regex],
        max_length=17,
        verbose_name="Telefonnummer"
    )
    strasse = models.CharField(max_length=200, verbose_name="Straße")
    plz = models.CharField(max_length=10, verbose_name="PLZ")
    ort = models.CharField(max_length=100, verbose_name="Ort")
    land = models.CharField(max_length=100, default="Deutschland", verbose_name="Land")
    datenschutz_akzeptiert = models.BooleanField(
        default=False,
        verbose_name="Datenschutzerklärung unterschrieben"
    )
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    aktualisiert_am = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")

    class Meta:
        verbose_name = "Kunde"
        verbose_name_plural = "Kunden"
        ordering = ['nachname', 'vorname']

    def __str__(self):
        return f"{self.vorname} {self.nachname}"

    def get_full_address(self):
        return f"{self.strasse}, {self.plz} {self.ort}, {self.land}"


class Raumtyp(models.Model):
    """Room Type model - Raumtypen"""
    EINZELZIMMER = 'EZ'
    DOPPELZIMMER = 'DZ'
    SUITE = 'SU'
    
    RAUMTYP_CHOICES = [
        (EINZELZIMMER, 'Einzelzimmer'),
        (DOPPELZIMMER, 'Doppelzimmer'),
        (SUITE, 'Suite'),
    ]
    
    name = models.CharField(max_length=50, verbose_name="Name")
    typ = models.CharField(
        max_length=2,
        choices=RAUMTYP_CHOICES,
        default=EINZELZIMMER,
        verbose_name="Typ"
    )
    beschreibung = models.TextField(blank=True, verbose_name="Beschreibung")
    preis_pro_nacht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preis pro Nacht"
    )

    class Meta:
        verbose_name = "Raumtyp"
        verbose_name_plural = "Raumtypen"

    def __str__(self):
        return f"{self.name} ({self.get_typ_display()})"


class Raum(models.Model):
    """Room model - Räume"""
    nummer = models.CharField(max_length=10, unique=True, verbose_name="Raumnummer")
    name = models.CharField(max_length=100, verbose_name="Name")
    raumtyp = models.ForeignKey(
        Raumtyp,
        on_delete=models.PROTECT,
        related_name='raeume',
        verbose_name="Raumtyp"
    )
    kapazitaet = models.IntegerField(default=1, verbose_name="Kapazität")
    ist_aktiv = models.BooleanField(default=True, verbose_name="Ist aktiv")
    beschreibung = models.TextField(blank=True, verbose_name="Beschreibung")

    class Meta:
        verbose_name = "Raum"
        verbose_name_plural = "Räume"
        ordering = ['nummer']

    def __str__(self):
        return f"Raum {self.nummer} - {self.name}"

    def ist_verfuegbar(self, start_datum, end_datum):
        """Check if room is available for the given date range"""
        konflikte = Buchung.objects.filter(
            raum=self,
            status__in=['optimierung', 'bestaetigt'],
            abreise_datum__gt=start_datum,
            anreise_datum__lt=end_datum
        )
        return not konflikte.exists()


class Buchung(models.Model):
    """Booking model - Buchungen"""
    STATUS_CHOICES = [
        ('optimierung', 'Optimierung'),
        ('bestaetigt', 'Bestätigt'),
        ('storniert', 'Storniert'),
    ]
    
    kunde = models.ForeignKey(
        Kunde,
        on_delete=models.CASCADE,
        related_name='buchungen',
        verbose_name="Kunde"
    )
    raum = models.ForeignKey(
        Raum,
        on_delete=models.PROTECT,
        related_name='buchungen',
        verbose_name="Raum"
    )
    anreise_datum = models.DateField(verbose_name="Anreise Datum")
    abreise_datum = models.DateField(verbose_name="Abreise Datum")
    checkin_zeit = models.TimeField(default="14:00", verbose_name="Check-in Zeit")
    checkout_zeit = models.TimeField(default="11:00", verbose_name="Check-out Zeit")
    anlass = models.CharField(max_length=200, verbose_name="Anlass")
    art_der_buchung = models.CharField(max_length=100, verbose_name="Art der Buchung")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='optimierung',
        verbose_name="Status"
    )
    buchungsnummer = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name="Buchungsnummer"
    )
    anzahl_teilnehmer = models.IntegerField(default=1, verbose_name="Anzahl Teilnehmer")
    anzahl_naechte = models.IntegerField(blank=True, null=True, verbose_name="Anzahl Nächte")
    veranstalter_name = models.CharField(max_length=200, blank=True, verbose_name="Veranstalter Name")
    veranstalter_kontakt = models.CharField(max_length=200, blank=True, verbose_name="Veranstalter Kontakt")
    erstellt_von = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='erstellte_buchungen',
        verbose_name="Erstellt von"
    )
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    aktualisiert_am = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    notizen = models.TextField(blank=True, verbose_name="Notizen")

    class Meta:
        verbose_name = "Buchung"
        verbose_name_plural = "Buchungen"
        ordering = ['-erstellt_am']

    def __str__(self):
        return f"Buchung {self.buchungsnummer} - {self.kunde}"

    def save(self, *args, **kwargs):
        if not self.buchungsnummer:
            # Generate booking number: BU-YYYYMMDD-XXX
            import random
            today = timezone.now().strftime('%Y%m%d')
            random_num = random.randint(100, 999)
            self.buchungsnummer = f"BU-{today}-{random_num}"
        
        # Calculate number of nights
        if self.anreise_datum and self.abreise_datum:
            delta = self.abreise_datum - self.anreise_datum
            self.anzahl_naechte = delta.days
        
        super().save(*args, **kwargs)

    def get_gesamtpreis(self):
        """Calculate total price for booking"""
        if self.anzahl_naechte and self.raum:
            raumpreis = self.raum.raumtyp.preis_pro_nacht * self.anzahl_naechte
            # Add additional charges from Belegungsprotokoll
            zusatzkosten = sum(
                posten.gesamtbetrag 
                for posten in self.belegungsprotokoll_set.all()
            )
            return raumpreis + zusatzkosten
        return 0


class Belegungsprotokoll(models.Model):
    """Occupancy Protocol - Belegungsprotokoll"""
    buchung = models.ForeignKey(
        Buchung,
        on_delete=models.CASCADE,
        verbose_name="Buchung"
    )
    leistung = models.CharField(max_length=200, verbose_name="Leistung")
    datum = models.DateField(verbose_name="Datum")
    anzahl = models.IntegerField(default=1, verbose_name="Anzahl/Menge")
    einzelpreis = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Einzelpreis"
    )
    gesamtbetrag = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        verbose_name="Gesamtbetrag"
    )
    schaden_vorher = models.TextField(blank=True, verbose_name="Schaden vorher")
    schaden_nachher = models.TextField(blank=True, verbose_name="Schaden nachher")
    notizen = models.TextField(blank=True, verbose_name="Notizen")

    class Meta:
        verbose_name = "Belegungsprotokoll"
        verbose_name_plural = "Belegungsprotokolle"

    def __str__(self):
        return f"{self.leistung} - {self.buchung.buchungsnummer}"

    def save(self, *args, **kwargs):
        self.gesamtbetrag = self.einzelpreis * self.anzahl
        super().save(*args, **kwargs)


class Rechnung(models.Model):
    """Invoice model - Rechnungen"""
    STATUS_CHOICES = [
        ('entwurf', 'Entwurf'),
        ('fertig', 'Fertig'),
        ('bezahlt', 'Bezahlt'),
    ]
    
    buchung = models.ForeignKey(
        Buchung,
        on_delete=models.CASCADE,
        related_name='rechnungen',
        verbose_name="Buchung"
    )
    rechnungsnummer = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name="Rechnungsnummer"
    )
    rechnungsdatum = models.DateField(default=timezone.now, verbose_name="Rechnungsdatum")
    faelligkeitsdatum = models.DateField(verbose_name="Fälligkeitsdatum")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='entwurf',
        verbose_name="Status"
    )
    gesamtbetrag = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Gesamtbetrag"
    )
    kommentar = models.TextField(blank=True, verbose_name="Kommentar")
    erstellt_von = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Erstellt von"
    )
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    aktualisiert_am = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")

    class Meta:
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"
        ordering = ['-erstellt_am']

    def __str__(self):
        return f"Rechnung {self.rechnungsnummer}"

    def save(self, *args, **kwargs):
        if not self.rechnungsnummer:
            # Generate invoice number: RE-YYYYMMDD-XXX
            import random
            today = timezone.now().strftime('%Y%m%d')
            random_num = random.randint(100, 999)
            self.rechnungsnummer = f"RE-{today}-{random_num}"
        super().save(*args, **kwargs)

    def berechne_gesamtbetrag(self):
        """Calculate total amount from booking and additional items"""
        return self.buchung.get_gesamtpreis()


class Rechnungsposten(models.Model):
    """Invoice line item - Rechnungsposten"""
    rechnung = models.ForeignKey(
        Rechnung,
        on_delete=models.CASCADE,
        related_name='posten',
        verbose_name="Rechnung"
    )
    beschreibung = models.CharField(max_length=200, verbose_name="Beschreibung")
    menge = models.IntegerField(default=1, verbose_name="Menge")
    einzelpreis = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Einzelpreis"
    )
    gesamtpreis = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        verbose_name="Gesamtpreis"
    )

    class Meta:
        verbose_name = "Rechnungsposten"
        verbose_name_plural = "Rechnungsposten"

    def __str__(self):
        return f"{self.beschreibung} - {self.rechnung.rechnungsnummer}"

    def save(self, *args, **kwargs):
        self.gesamtpreis = self.einzelpreis * self.menge
        super().save(*args, **kwargs)
