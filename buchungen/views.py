from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Kunde, Raum, Raumtyp, Buchung, Rechnung, Rechnungsposten, Belegungsprotokoll
from .forms import KundeForm, BuchungForm, RechnungForm
import json


@login_required
def dashboard(request):
    """Dashboard view - Main entry point"""
    heute = timezone.now().date()
    
    context = {
        'total_kunden': Kunde.objects.count(),
        'total_buchungen': Buchung.objects.count(),
        'aktuelle_buchungen': Buchung.objects.filter(
            anreise_datum__lte=heute,
            abreise_datum__gte=heute,
            status='bestaetigt'
        ).count(),
        'verfuegbare_raeume': Raum.objects.filter(ist_aktiv=True).count(),
    }
    return render(request, 'buchungen/dashboard.html', context)


@login_required
def kunde_liste(request):
    """Customer list view - Kundenübersicht"""
    kunden = Kunde.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        kunden = kunden.filter(
            Q(vorname__icontains=search_query) |
            Q(nachname__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telefonnummer__icontains=search_query)
        )
    
    return render(request, 'buchungen/kunde_liste.html', {'kunden': kunden, 'search_query': search_query})


@login_required
def kunde_anlegen(request):
    """Create new customer - Neuer Kunde anlegen"""
    if request.method == 'POST':
        form = KundeForm(request.POST)
        if form.is_valid():
            kunde = form.save()
            messages.success(request, f'Der Kunde {kunde.vorname} {kunde.nachname} wurde erfolgreich angelegt.')
            return redirect('kunde_liste')
        else:
            messages.error(request, 'Bitte füllen Sie alle Pflichtfelder aus.')
    else:
        form = KundeForm()
    
    return render(request, 'buchungen/kunde_form.html', {'form': form, 'title': 'Neuer Kunde'})


@login_required
def kunde_bearbeiten(request, pk):
    """Edit customer"""
    kunde = get_object_or_404(Kunde, pk=pk)
    
    if request.method == 'POST':
        form = KundeForm(request.POST, instance=kunde)
        if form.is_valid():
            form.save()
            messages.success(request, f'Der Kunde {kunde.vorname} {kunde.nachname} wurde erfolgreich aktualisiert.')
            return redirect('kunde_liste')
    else:
        form = KundeForm(instance=kunde)
    
    return render(request, 'buchungen/kunde_form.html', {'form': form, 'title': 'Kunde bearbeiten', 'kunde': kunde})


@login_required
def kunde_detail(request, pk):
    """Customer detail view"""
    kunde = get_object_or_404(Kunde, pk=pk)
    buchungen = kunde.buchungen.all()
    return render(request, 'buchungen/kunde_detail.html', {'kunde': kunde, 'buchungen': buchungen})


@login_required
def buchung_liste(request):
    """Booking list view"""
    buchungen = Buchung.objects.select_related('kunde', 'raum').all()
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        buchungen = buchungen.filter(status=status)
    
    return render(request, 'buchungen/buchung_liste.html', {'buchungen': buchungen})


@login_required
def buchung_erstellen(request):
    """Create new booking - Neuer Vorgang"""
    if request.method == 'POST':
        form = BuchungForm(request.POST)
        if form.is_valid():
            buchung = form.save(commit=False)
            buchung.erstellt_von = request.user
            buchung.save()
            messages.success(request, f'Die Buchung {buchung.buchungsnummer} wurde erfolgreich erstellt.')
            return redirect('buchung_detail', pk=buchung.pk)
    else:
        form = BuchungForm()
    
    return render(request, 'buchungen/buchung_form.html', {'form': form, 'title': 'Neue Buchung'})


@login_required
def buchung_detail(request, pk):
    """Booking detail view"""
    buchung = get_object_or_404(Buchung, pk=pk)
    belegungsprotokolle = buchung.belegungsprotokoll_set.all()
    rechnungen = buchung.rechnungen.all()
    
    context = {
        'buchung': buchung,
        'belegungsprotokolle': belegungsprotokolle,
        'rechnungen': rechnungen,
        'gesamtpreis': buchung.get_gesamtpreis(),
    }
    return render(request, 'buchungen/buchung_detail.html', context)


@login_required
def buchung_bearbeiten(request, pk):
    """Edit booking"""
    buchung = get_object_or_404(Buchung, pk=pk)
    
    if request.method == 'POST':
        form = BuchungForm(request.POST, instance=buchung)
        if form.is_valid():
            form.save()
            messages.success(request, f'Die Buchung {buchung.buchungsnummer} wurde erfolgreich aktualisiert.')
            return redirect('buchung_detail', pk=buchung.pk)
    else:
        form = BuchungForm(instance=buchung)
    
    return render(request, 'buchungen/buchung_form.html', {'form': form, 'title': 'Buchung bearbeiten', 'buchung': buchung})


@login_required
def kalender_uebersicht(request):
    """Calendar overview - Kalenderübersicht"""
    # Get current week
    heute = timezone.now().date()
    wochenstart = heute - timedelta(days=heute.weekday())
    wochenende = wochenstart + timedelta(days=6)
    
    # Get all active rooms
    raeume = Raum.objects.filter(ist_aktiv=True)
    
    # Get bookings for current week
    buchungen = Buchung.objects.filter(
        status__in=['optimierung', 'bestaetigt'],
        abreise_datum__gte=wochenstart,
        anreise_datum__lte=wochenende
    ).select_related('kunde', 'raum')
    
    # Create calendar data structure
    kalenderdaten = []
    current_date = wochenstart
    while current_date <= wochenende:
        tag_buchungen = []
        for raum in raeume:
            raum_buchungen = buchungen.filter(
                raum=raum,
                anreise_datum__lte=current_date,
                abreise_datum__gt=current_date
            )
            tag_buchungen.append({
                'raum': raum,
                'buchungen': raum_buchungen
            })
        
        kalenderdaten.append({
            'datum': current_date,
            'ist_heute': current_date == heute,
            'raum_buchungen': tag_buchungen
        })
        current_date += timedelta(days=1)
    
    context = {
        'kalenderdaten': kalenderdaten,
        'wochenstart': wochenstart,
        'wochenende': wochenende,
        'heute': heute,
    }
    return render(request, 'buchungen/kalender_uebersicht.html', context)


@login_required
def raum_verfuegbarkeit(request):
    """Check room availability - AJAX endpoint"""
    if request.method == 'GET':
        start_datum_str = request.GET.get('start_datum')
        end_datum_str = request.GET.get('end_datum')
        
        if start_datum_str and end_datum_str:
            start_datum = datetime.strptime(start_datum_str, '%Y-%m-%d').date()
            end_datum = datetime.strptime(end_datum_str, '%Y-%m-%d').date()
            
            verfuegbare_raeume = []
            for raum in Raum.objects.filter(ist_aktiv=True):
                if raum.ist_verfuegbar(start_datum, end_datum):
                    verfuegbare_raeume.append({
                        'id': raum.id,
                        'nummer': raum.nummer,
                        'name': raum.name,
                        'typ': raum.raumtyp.name,
                        'preis': str(raum.raumtyp.preis_pro_nacht)
                    })
            
            return JsonResponse({'verfuegbare_raeume': verfuegbare_raeume})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def rechnung_erstellen(request, buchung_pk):
    """Create invoice for booking - Rechnung erstellen"""
    buchung = get_object_or_404(Buchung, pk=buchung_pk)
    
    if request.method == 'POST':
        form = RechnungForm(request.POST)
        if form.is_valid():
            rechnung = form.save(commit=False)
            rechnung.buchung = buchung
            rechnung.erstellt_von = request.user
            rechnung.save()
            
            # Create invoice items from booking
            if buchung.raum and buchung.anzahl_naechte:
                Rechnungsposten.objects.create(
                    rechnung=rechnung,
                    beschreibung=f"Raum {buchung.raum.nummer} - {buchung.anzahl_naechte} Nächte",
                    menge=buchung.anzahl_naechte,
                    einzelpreis=buchung.raum.raumtyp.preis_pro_nacht
                )
            
            # Add items from Belegungsprotokoll
            for protokoll in buchung.belegungsprotokoll_set.all():
                Rechnungsposten.objects.create(
                    rechnung=rechnung,
                    beschreibung=protokoll.leistung,
                    menge=protokoll.anzahl,
                    einzelpreis=protokoll.einzelpreis
                )
            
            # Calculate total
            rechnung.gesamtbetrag = rechnung.berechne_gesamtbetrag()
            rechnung.save()
            
            messages.success(request, f'Die Rechnung {rechnung.rechnungsnummer} wurde erfolgreich erstellt.')
            return redirect('rechnung_detail', pk=rechnung.pk)
    else:
        form = RechnungForm(initial={'buchung': buchung})
    
    return render(request, 'buchungen/rechnung_form.html', {'form': form, 'buchung': buchung, 'title': 'Neue Rechnung'})


@login_required
def rechnung_detail(request, pk):
    """Invoice detail view"""
    rechnung = get_object_or_404(Rechnung, pk=pk)
    posten = rechnung.posten.all()
    
    context = {
        'rechnung': rechnung,
        'posten': posten,
        'kunde': rechnung.buchung.kunde,
    }
    return render(request, 'buchungen/rechnung_detail.html', context)


@login_required
def rechnung_pdf(request, pk):
    """Generate PDF invoice"""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    from io import BytesIO
    
    rechnung = get_object_or_404(Rechnung, pk=pk)
    kunde = rechnung.buchung.kunde
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(2*cm, height - 2*cm, "Passat Buchungssystem")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(2*cm, height - 3*cm, "RECHNUNG")
    
    # Invoice details
    p.setFont("Helvetica", 10)
    y_position = height - 4*cm
    p.drawString(2*cm, y_position, f"Rechnungsnummer: {rechnung.rechnungsnummer}")
    y_position -= 0.5*cm
    p.drawString(2*cm, y_position, f"Rechnungsdatum: {rechnung.rechnungsdatum.strftime('%d.%m.%Y')}")
    y_position -= 0.5*cm
    p.drawString(2*cm, y_position, f"Fälligkeitsdatum: {rechnung.faelligkeitsdatum.strftime('%d.%m.%Y')}")
    
    # Customer details
    y_position -= 1.5*cm
    p.setFont("Helvetica-Bold", 11)
    p.drawString(2*cm, y_position, "Kunde:")
    y_position -= 0.5*cm
    p.setFont("Helvetica", 10)
    p.drawString(2*cm, y_position, f"{kunde.vorname} {kunde.nachname}")
    y_position -= 0.5*cm
    p.drawString(2*cm, y_position, kunde.strasse)
    y_position -= 0.5*cm
    p.drawString(2*cm, y_position, f"{kunde.plz} {kunde.ort}")
    
    # Invoice items
    y_position -= 1.5*cm
    p.setFont("Helvetica-Bold", 11)
    p.drawString(2*cm, y_position, "Rechnungsposten:")
    y_position -= 0.7*cm
    
    p.setFont("Helvetica-Bold", 9)
    p.drawString(2*cm, y_position, "Beschreibung")
    p.drawString(10*cm, y_position, "Menge")
    p.drawString(12*cm, y_position, "Einzelpreis")
    p.drawString(15*cm, y_position, "Gesamtpreis")
    y_position -= 0.5*cm
    
    p.setFont("Helvetica", 9)
    for posten in rechnung.posten.all():
        p.drawString(2*cm, y_position, posten.beschreibung[:40])
        p.drawString(10*cm, y_position, str(posten.menge))
        p.drawString(12*cm, y_position, f"€ {posten.einzelpreis:.2f}")
        p.drawString(15*cm, y_position, f"€ {posten.gesamtpreis:.2f}")
        y_position -= 0.5*cm
    
    # Total
    y_position -= 0.5*cm
    p.setFont("Helvetica-Bold", 11)
    p.drawString(12*cm, y_position, "Gesamtbetrag:")
    p.drawString(15*cm, y_position, f"€ {rechnung.gesamtbetrag:.2f}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Rechnung_{rechnung.rechnungsnummer}.pdf"'
    
    return response


@login_required
def kunde_suche_ajax(request):
    """AJAX endpoint for customer autocomplete"""
    query = request.GET.get('q', '')
    if query:
        kunden = Kunde.objects.filter(
            Q(vorname__icontains=query) |
            Q(nachname__icontains=query)
        )[:10]
        
        results = [{
            'id': kunde.id,
            'name': f"{kunde.vorname} {kunde.nachname}",
            'email': kunde.email
        } for kunde in kunden]
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})


@login_required
def raum_suche_ajax(request):
    """AJAX endpoint for room autocomplete"""
    query = request.GET.get('q', '')
    if query:
        raeume = Raum.objects.filter(
            Q(nummer__icontains=query) |
            Q(name__icontains=query),
            ist_aktiv=True
        )[:10]
        
        results = [{
            'id': raum.id,
            'nummer': raum.nummer,
            'name': raum.name,
            'typ': raum.raumtyp.name
        } for raum in raeume]
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})
