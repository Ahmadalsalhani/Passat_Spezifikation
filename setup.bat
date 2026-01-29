@echo off
REM Passat Buchungssystem - Automatisches Setup-Skript für Windows

echo ===============================================================
echo    Passat Buchungssystem - Automatische Installation
echo ===============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python ist nicht installiert!
    echo Bitte installieren Sie Python 3.8 oder hoeher von python.org
    pause
    exit /b 1
)

echo [OK] Python gefunden
echo.

REM Install dependencies
echo [1/3] Installiere Abhaengigkeiten...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [X] Fehler beim Installieren der Abhaengigkeiten
    pause
    exit /b 1
)
echo [OK] Abhaengigkeiten erfolgreich installiert
echo.

REM Run migrations
echo [2/3] Richte Datenbank ein...
python manage.py migrate --no-input
if errorlevel 1 (
    echo [X] Fehler beim Einrichten der Datenbank
    pause
    exit /b 1
)
echo [OK] Datenbank erfolgreich eingerichtet
echo.

REM Load sample data
echo [3/3] Lade Beispieldaten...
python manage.py load_sample_data
if errorlevel 1 (
    echo [X] Fehler beim Laden der Beispieldaten
    pause
    exit /b 1
)
echo [OK] Beispieldaten erfolgreich geladen
echo.

echo ===============================================================
echo             Installation erfolgreich abgeschlossen!
echo ===============================================================
echo.
echo Starten Sie den Server mit:
echo    python manage.py runserver
echo.
echo Oeffnen Sie dann im Browser:
echo    http://127.0.0.1:8000/
echo.
echo Login-Daten:
echo    Benutzername: admin
echo    Passwort: admin123
echo.
echo Weitere Informationen:
echo    - QUICKSTART.md - Schnellstart-Anleitung
echo    - README_DJANGO.md - Vollstaendige Dokumentation
echo    - PROJEKT_UEBERSICHT.md - Projekt-Uebersicht
echo.
pause
