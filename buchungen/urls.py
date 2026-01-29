from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Customer URLs
    path('kunden/', views.kunde_liste, name='kunde_liste'),
    path('kunden/neu/', views.kunde_anlegen, name='kunde_anlegen'),
    path('kunden/<int:pk>/', views.kunde_detail, name='kunde_detail'),
    path('kunden/<int:pk>/bearbeiten/', views.kunde_bearbeiten, name='kunde_bearbeiten'),
    
    # Booking URLs
    path('buchungen/', views.buchung_liste, name='buchung_liste'),
    path('buchungen/neu/', views.buchung_erstellen, name='buchung_erstellen'),
    path('buchungen/<int:pk>/', views.buchung_detail, name='buchung_detail'),
    path('buchungen/<int:pk>/bearbeiten/', views.buchung_bearbeiten, name='buchung_bearbeiten'),
    
    # Calendar
    path('kalender/', views.kalender_uebersicht, name='kalender_uebersicht'),
    
    # Invoice URLs
    path('buchungen/<int:buchung_pk>/rechnung/neu/', views.rechnung_erstellen, name='rechnung_erstellen'),
    path('rechnungen/<int:pk>/', views.rechnung_detail, name='rechnung_detail'),
    path('rechnungen/<int:pk>/pdf/', views.rechnung_pdf, name='rechnung_pdf'),
    
    # AJAX URLs
    path('ajax/raum-verfuegbarkeit/', views.raum_verfuegbarkeit, name='raum_verfuegbarkeit'),
    path('ajax/kunde-suche/', views.kunde_suche_ajax, name='kunde_suche_ajax'),
    path('ajax/raum-suche/', views.raum_suche_ajax, name='raum_suche_ajax'),
]
