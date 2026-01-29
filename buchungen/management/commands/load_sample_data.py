from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from buchungen.models import Kunde, Raumtyp, Raum, Buchung
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Lädt Beispieldaten für das Passat Buchungssystem'

    def handle(self, *args, **options):
        self.stdout.write('Lade Beispieldaten...')
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@passat.de', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin-Benutzer erstellt: admin/admin123'))
        
        # Create Raumtypen
        einzelzimmer, _ = Raumtyp.objects.get_or_create(
            name='Einzelzimmer',
            typ='EZ',
            defaults={'preis_pro_nacht': 89.00, 'beschreibung': 'Gemütliches Einzelzimmer'}
        )
        doppelzimmer, _ = Raumtyp.objects.get_or_create(
            name='Doppelzimmer',
            typ='DZ',
            defaults={'preis_pro_nacht': 129.00, 'beschreibung': 'Komfortables Doppelzimmer'}
        )
        suite, _ = Raumtyp.objects.get_or_create(
            name='Kapitäns-Suite',
            typ='SU',
            defaults={'preis_pro_nacht': 199.00, 'beschreibung': 'Luxuriöse Suite mit Meerblick'}
        )
        self.stdout.write(self.style.SUCCESS('Raumtypen erstellt'))
        
        # Create Räume
        raeume_data = [
            ('101', 'Backbord Vorne', einzelzimmer, 1),
            ('102', 'Steuerbord Vorne', einzelzimmer, 1),
            ('201', 'Backbord Mitte', doppelzimmer, 2),
            ('202', 'Steuerbord Mitte', doppelzimmer, 2),
            ('301', 'Kapitäns-Suite', suite, 2),
        ]
        
        for nummer, name, raumtyp, kapazitaet in raeume_data:
            Raum.objects.get_or_create(
                nummer=nummer,
                defaults={
                    'name': name,
                    'raumtyp': raumtyp,
                    'kapazitaet': kapazitaet,
                    'ist_aktiv': True
                }
            )
        self.stdout.write(self.style.SUCCESS('Räume erstellt'))
        
        # Create Kunden
        kunden_data = [
            ('Max', 'Mustermann', 'max@example.com', '+491701234567', 'Musterstraße 1', '12345', 'Musterstadt', 'Deutschland'),
            ('Erika', 'Beispiel', 'erika@example.com', '+491702345678', 'Beispielweg 2', '23456', 'Beispielort', 'Deutschland'),
            ('Hans', 'Schmidt', 'hans@example.com', '+491703456789', 'Schmidtstraße 3', '34567', 'Hansestadt', 'Deutschland'),
        ]
        
        for vorname, nachname, email, telefon, strasse, plz, ort, land in kunden_data:
            Kunde.objects.get_or_create(
                email=email,
                defaults={
                    'vorname': vorname,
                    'nachname': nachname,
                    'telefonnummer': telefon,
                    'strasse': strasse,
                    'plz': plz,
                    'ort': ort,
                    'land': land,
                    'datenschutz_akzeptiert': True
                }
            )
        self.stdout.write(self.style.SUCCESS('Kunden erstellt'))
        
        # Create sample bookings
        admin_user = User.objects.get(username='admin')
        kunde1 = Kunde.objects.get(email='max@example.com')
        kunde2 = Kunde.objects.get(email='erika@example.com')
        raum1 = Raum.objects.get(nummer='101')
        raum2 = Raum.objects.get(nummer='201')
        
        heute = date.today()
        
        # Booking 1 - Current
        if not Buchung.objects.filter(kunde=kunde1, raum=raum1).exists():
            Buchung.objects.create(
                kunde=kunde1,
                raum=raum1,
                anreise_datum=heute,
                abreise_datum=heute + timedelta(days=3),
                anlass='Geschäftsreise',
                art_der_buchung='Standard',
                status='bestaetigt',
                anzahl_teilnehmer=1,
                erstellt_von=admin_user
            )
        
        # Booking 2 - Future
        if not Buchung.objects.filter(kunde=kunde2, raum=raum2).exists():
            Buchung.objects.create(
                kunde=kunde2,
                raum=raum2,
                anreise_datum=heute + timedelta(days=7),
                abreise_datum=heute + timedelta(days=10),
                anlass='Urlaub',
                art_der_buchung='Standard',
                status='optimierung',
                anzahl_teilnehmer=2,
                erstellt_von=admin_user
            )
        
        self.stdout.write(self.style.SUCCESS('Beispiel-Buchungen erstellt'))
        
        self.stdout.write(self.style.SUCCESS('Alle Beispieldaten erfolgreich geladen!'))
        self.stdout.write(self.style.WARNING('Login: admin / Passwort: admin123'))
