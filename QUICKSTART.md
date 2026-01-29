# Passat Buchungssystem - Quick Start Guide

## Schnellstart (5 Minuten)

### 1. Installation

```bash
# Python-Pakete installieren
pip install -r requirements.txt

# Datenbank einrichten
python manage.py migrate

# Beispieldaten laden (inkl. Admin-Benutzer)
python manage.py load_sample_data
```

### 2. Server starten

```bash
python manage.py runserver
```

### 3. Zugriff

- **Hauptanwendung**: http://127.0.0.1:8000/
- **Admin-Interface**: http://127.0.0.1:8000/admin/

**Login-Daten:**
- Benutzername: `admin`
- Passwort: `admin123`

## Was wurde geladen?

Die Beispieldaten enthalten:

### Raumtypen
- Einzelzimmer (89 € pro Nacht)
- Doppelzimmer (129 € pro Nacht)
- Kapitäns-Suite (199 € pro Nacht)

### Räume
- Raum 101 - Backbord Vorne (Einzelzimmer)
- Raum 102 - Steuerbord Vorne (Einzelzimmer)
- Raum 201 - Backbord Mitte (Doppelzimmer)
- Raum 202 - Steuerbord Mitte (Doppelzimmer)
- Raum 301 - Kapitäns-Suite (Suite)

### Kunden
- Max Mustermann
- Erika Beispiel
- Hans Schmidt

### Buchungen
- 2 Beispiel-Buchungen (aktuelle und zukünftige)

## Hauptfunktionen testen

### 1. Dashboard
Besuchen Sie http://127.0.0.1:8000/ um die Übersicht zu sehen.

### 2. Neuen Kunden anlegen
1. Klicken Sie auf "Neuer Kunde anlegen"
2. Füllen Sie das Formular aus
3. Aktivieren Sie die Datenschutz-Checkbox
4. Klicken Sie "Speichern"

### 3. Neue Buchung erstellen
1. Klicken Sie auf "Neue Buchung erstellen"
2. Wählen Sie einen Kunden
3. Geben Sie Daten ein
4. Wählen Sie einen freien Raum
5. Klicken Sie "Speichern"

### 4. Kalenderübersicht
Klicken Sie im Menü auf "Kalenderübersicht" um alle Buchungen der Woche zu sehen.

### 5. Rechnung erstellen
1. Öffnen Sie eine Buchung
2. Klicken Sie "Rechnung erstellen"
3. Legen Sie das Fälligkeitsdatum fest
4. Erstellen Sie die Rechnung
5. Laden Sie die PDF herunter

## Admin-Interface

Unter http://127.0.0.1:8000/admin/ haben Sie vollen Zugriff auf:
- Benutzerverwaltung
- Alle Datenbankeinträge
- Erweiterte Bearbeitungsfunktionen

## Tipps

### Eigene Daten hinzufügen
Verwenden Sie das Admin-Interface oder die Weboberfläche, um weitere Räume, Kunden und Buchungen hinzuzufügen.

### Produktiv einsetzen
Für den Produktiveinsatz:
1. Ändern Sie das Admin-Passwort
2. Setzen Sie in `settings.py`: `DEBUG = False`
3. Konfigurieren Sie `ALLOWED_HOSTS`
4. Verwenden Sie PostgreSQL statt SQLite
5. Richten Sie einen Webserver (nginx + gunicorn) ein

### Bei Problemen
```bash
# Datenbank zurücksetzen
rm db.sqlite3
python manage.py migrate
python manage.py load_sample_data

# Server-Logs prüfen
python manage.py runserver
```

## Nächste Schritte

Lesen Sie die vollständige Dokumentation in `README_DJANGO.md` für:
- Detaillierte Funktionsbeschreibungen
- Deployment-Anleitung
- Sicherheitshinweise
- Entwicklungs-Tipps

## Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im GitHub-Repository.

---

Viel Erfolg mit dem Passat Buchungssystem! 🚢
