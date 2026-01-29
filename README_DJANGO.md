# Passat Buchungssystem - Django Webanwendung

Eine Django-basierte Webanwendung zur Verwaltung von Kunden, Buchungen und Rechnungen für das Schiff "Passat" in Travemünde.

## Projektbeschreibung

Das Passat Buchungssystem ist ein internes Verwaltungstool für die Mitarbeiter des Schiffs "Passat". Es dient zur zentralen Erfassung und Verwaltung von:

- **Kundendaten** - Verwaltung von Kunden mit vollständigen Stammdaten
- **Raum- und Belegungsplanung** - Übersicht über alle Räume und deren Verfügbarkeit
- **Buchungen** - Erstellung und Verwaltung von Buchungen mit Kalenderübersicht
- **Rechnungsstellung** - Automatische Rechnungserstellung und PDF-Export

## Funktionen

### Kundenverwaltung
- Neue Kunden anlegen mit Pflichtfeldern (Vorname, Nachname, E-Mail, Telefon, Adresse)
- Kundenübersicht mit Suchfunktion
- Datenschutzerklärung muss akzeptiert werden
- Vollständige CRUD-Operationen für Kundendaten

### Buchungsverwaltung
- Neue Buchungen mit An- und Abreisedatum erstellen
- Check-in und Check-out Zeiten festlegen
- Raumauswahl mit automatischer Verfügbarkeitsprüfung
- Buchungsstatus (Optimierung, Bestätigt, Storniert)
- Automatische Berechnung der Anzahl Nächte
- Veranstalterdaten erfassen
- Belegungsprotokolle mit Zusatzleistungen

### Raumverwaltung
- Verschiedene Raumtypen (Einzelzimmer, Doppelzimmer, Suite)
- Raumverwaltung mit Nummern, Namen und Kapazität
- Preise pro Nacht konfigurierbar
- Räume aktivieren/deaktivieren

### Kalenderübersicht
- Wochenübersicht aller Buchungen
- Farbliche Unterscheidung: Frei/Belegt
- Aktuelle Tag hervorgehoben
- Kundenname und Raum direkt im Kalender sichtbar

### Rechnungswesen
- Automatische Rechnungserstellung aus Buchungen
- Rechnungsposten mit Menge und Einzelpreis
- Automatische Gesamtberechnung
- PDF-Export für Rechnungen
- Fälligkeitsdatum und Status-Tracking

### Benutzer und Rollen
- **Admin**: Vollzugriff auf System, Benutzerverwaltung
- **User**: Mitarbeiter mit Zugriff auf Kunden- und Buchungsverwaltung
- Externe Personen haben keinen Zugriff

## Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritt 1: Repository klonen

```bash
git clone <repository-url>
cd Passat_Spezifikation
```

### Schritt 2: Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

### Schritt 3: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Schritt 4: Datenbank migrieren

```bash
python manage.py makemigrations
python manage.py migrate
```

### Schritt 5: Admin-Benutzer erstellen

```bash
python manage.py createsuperuser
```

Folgen Sie den Anweisungen und erstellen Sie einen Administrator-Account.

### Schritt 6: Server starten

```bash
python manage.py runserver
```

Die Anwendung ist nun unter `http://127.0.0.1:8000/` erreichbar.

## Verwendung

### 1. Erste Schritte

1. Öffnen Sie `http://127.0.0.1:8000/admin/` und melden Sie sich mit dem Admin-Account an
2. Erstellen Sie Raumtypen unter "Raumtypen"
3. Erstellen Sie Räume unter "Räume"
4. Kehren Sie zur Hauptanwendung zurück unter `http://127.0.0.1:8000/`

### 2. Neuen Kunden anlegen

1. Klicken Sie auf "Neuer Kunde anlegen" im Dashboard
2. Füllen Sie alle Pflichtfelder aus:
   - Vorname
   - Nachname
   - E-Mail
   - Telefonnummer
   - Straße
   - PLZ
   - Ort
   - Land
3. Akzeptieren Sie die Datenschutzerklärung (Checkbox)
4. Klicken Sie auf "Speichern"

Der Kunde erscheint nun in der Kundenübersicht.

### 3. Neue Buchung erstellen

1. Klicken Sie auf "Neue Buchung erstellen" im Dashboard
2. Wählen Sie einen Kunden aus
3. Geben Sie An- und Abreisedatum ein
4. Wählen Sie einen verfügbaren Raum
5. Geben Sie Anlass und Art der Buchung ein
6. Setzen Sie den Status (Standard: "Optimierung")
7. Optional: Fügen Sie Veranstalterinformationen hinzu
8. Klicken Sie auf "Speichern"

Die Buchung wird mit einer automatisch generierten Buchungsnummer erstellt.

### 4. Rechnung erstellen

1. Öffnen Sie eine Buchung in der Detailansicht
2. Klicken Sie auf "Rechnung erstellen"
3. Legen Sie das Fälligkeitsdatum fest
4. Die Rechnungsposten werden automatisch aus der Buchung übernommen
5. Klicken Sie auf "Rechnung erstellen"
6. In der Rechnungsdetailansicht können Sie die Rechnung als PDF herunterladen

### 5. Kalenderübersicht nutzen

1. Klicken Sie im Menü auf "Kalenderübersicht"
2. Sehen Sie alle Buchungen der aktuellen Woche
3. Freie Räume sind grün, belegte Räume rot markiert
4. Der heutige Tag ist gelb hervorgehoben
5. Klicken Sie auf eine Buchung für Details

## Admin-Interface

Das Django Admin-Interface ist unter `/admin/` verfügbar und bietet:

- Vollständige Verwaltung aller Daten
- Benutzer- und Rechteverwaltung
- Bulk-Operationen
- Erweiterte Filteroptionen
- Inline-Bearbeitung von verknüpften Objekten

## Technische Details

### Verwendete Technologien

- **Backend**: Django 6.0.1
- **Datenbank**: SQLite (Standard, kann auf PostgreSQL/MySQL umgestellt werden)
- **Frontend**: Bootstrap 5.1.3
- **Icons**: Bootstrap Icons
- **PDF-Generierung**: ReportLab 4.4.9

### Projektstruktur

```
Passat_Spezifikation/
├── buchungen/              # Hauptanwendung
│   ├── models.py          # Datenmodelle
│   ├── views.py           # Views/Controller
│   ├── forms.py           # Formulare
│   ├── admin.py           # Admin-Konfiguration
│   ├── urls.py            # URL-Routing
│   └── templates/         # HTML-Templates
│       └── buchungen/
├── passat_buchungssystem/ # Django-Projekteinstellungen
│   ├── settings.py        # Konfiguration
│   ├── urls.py            # Haupt-URL-Routing
│   └── wsgi.py            # WSGI-Konfiguration
├── manage.py              # Django Management-Tool
├── requirements.txt       # Python-Abhängigkeiten
└── README_DJANGO.md       # Diese Datei
```

### Datenmodelle

- **Kunde**: Kundenstammdaten
- **Raumtyp**: Definition von Raumtypen (Einzelzimmer, Doppelzimmer, Suite)
- **Raum**: Einzelne Räume mit Zuordnung zu Raumtypen
- **Buchung**: Buchungen mit Kunden- und Raumzuordnung
- **Belegungsprotokoll**: Zusatzleistungen und Kosten zu Buchungen
- **Rechnung**: Rechnungen mit Verknüpfung zu Buchungen
- **Rechnungsposten**: Einzelne Positionen einer Rechnung

## Sicherheit

- Alle sensiblen Operationen erfordern Login
- CSRF-Schutz aktiviert
- Datenschutzerklärung muss vor Datenspeicherung akzeptiert werden
- SQL-Injection-Schutz durch Django ORM
- XSS-Schutz durch Template-Escaping

## Entwicklung

### Tests ausführen

```bash
python manage.py test
```

### Neue Migration erstellen

```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files sammeln (für Production)

```bash
python manage.py collectstatic
```

## Deployment

Für ein Production-Deployment:

1. Ändern Sie `DEBUG = False` in `settings.py`
2. Setzen Sie einen sicheren `SECRET_KEY`
3. Konfigurieren Sie `ALLOWED_HOSTS`
4. Verwenden Sie eine Production-Datenbank (PostgreSQL empfohlen)
5. Konfigurieren Sie einen Webserver (nginx + gunicorn empfohlen)
6. Aktivieren Sie HTTPS

## Support und Weiterentwicklung

Für Fragen oder Probleme erstellen Sie bitte ein Issue im Repository.

## Lizenz

Dieses Projekt wurde für das Schiff "Passat" in Travemünde entwickelt.

---

© 2024 Passat Buchungssystem
