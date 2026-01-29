#!/bin/bash
# Passat Buchungssystem - Automatisches Setup-Skript

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Passat Buchungssystem - Automatische Installation     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "Bitte installieren Sie Python 3.8 oder höher."
    exit 1
fi

echo "✓ Python 3 gefunden: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installiere Abhängigkeiten..."
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✓ Abhängigkeiten erfolgreich installiert"
else
    echo "❌ Fehler beim Installieren der Abhängigkeiten"
    exit 1
fi
echo ""

# Run migrations
echo "🗄️  Richte Datenbank ein..."
python3 manage.py migrate --no-input
if [ $? -eq 0 ]; then
    echo "✓ Datenbank erfolgreich eingerichtet"
else
    echo "❌ Fehler beim Einrichten der Datenbank"
    exit 1
fi
echo ""

# Load sample data
echo "📊 Lade Beispieldaten..."
python3 manage.py load_sample_data
if [ $? -eq 0 ]; then
    echo "✓ Beispieldaten erfolgreich geladen"
else
    echo "❌ Fehler beim Laden der Beispieldaten"
    exit 1
fi
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║            ✅ Installation erfolgreich!                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Starten Sie den Server mit:"
echo "   python3 manage.py runserver"
echo ""
echo "🌐 Öffnen Sie dann im Browser:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "👤 Login-Daten:"
echo "   Benutzername: admin"
echo "   Passwort: admin123"
echo ""
echo "📚 Weitere Informationen:"
echo "   - QUICKSTART.md - Schnellstart-Anleitung"
echo "   - README_DJANGO.md - Vollständige Dokumentation"
echo "   - PROJEKT_UEBERSICHT.md - Projekt-Übersicht"
echo ""
