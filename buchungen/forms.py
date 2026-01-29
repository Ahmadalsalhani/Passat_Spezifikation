from django import forms
from .models import Kunde, Buchung, Rechnung
from datetime import timedelta


class KundeForm(forms.ModelForm):
    """Form for customer management"""
    
    class Meta:
        model = Kunde
        fields = ['vorname', 'nachname', 'email', 'telefonnummer', 'strasse', 'plz', 'ort', 'land', 'datenschutz_akzeptiert']
        widgets = {
            'vorname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vorname'}),
            'nachname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nachname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-Mail'}),
            'telefonnummer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+49...'}),
            'strasse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Straße'}),
            'plz': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PLZ'}),
            'ort': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ort'}),
            'land': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Land'}),
            'datenschutz_akzeptiert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        datenschutz = cleaned_data.get('datenschutz_akzeptiert')
        
        if not datenschutz:
            raise forms.ValidationError(
                'Die Datenschutzerklärung muss akzeptiert werden, bevor Kundendaten gespeichert werden dürfen.'
            )
        
        return cleaned_data


class BuchungForm(forms.ModelForm):
    """Form for booking management"""
    
    class Meta:
        model = Buchung
        fields = [
            'kunde', 'raum', 'anreise_datum', 'abreise_datum',
            'checkin_zeit', 'checkout_zeit', 'anlass', 'art_der_buchung',
            'status', 'anzahl_teilnehmer', 'veranstalter_name',
            'veranstalter_kontakt', 'notizen'
        ]
        widgets = {
            'kunde': forms.Select(attrs={'class': 'form-control'}),
            'raum': forms.Select(attrs={'class': 'form-control'}),
            'anreise_datum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'abreise_datum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'checkin_zeit': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'checkout_zeit': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'anlass': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Anlass der Buchung'}),
            'art_der_buchung': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Art der Buchung'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'anzahl_teilnehmer': forms.NumberInput(attrs={'class': 'form-control'}),
            'veranstalter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veranstalter Name'}),
            'veranstalter_kontakt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon/E-Mail'}),
            'notizen': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        anreise = cleaned_data.get('anreise_datum')
        abreise = cleaned_data.get('abreise_datum')
        raum = cleaned_data.get('raum')
        
        if anreise and abreise:
            if abreise <= anreise:
                raise forms.ValidationError('Das Abreisedatum muss nach dem Anreisedatum liegen.')
            
            # Check room availability
            if raum and not raum.ist_verfuegbar(anreise, abreise):
                raise forms.ValidationError(
                    f'Der Raum {raum.nummer} ist für den gewählten Zeitraum nicht verfügbar.'
                )
        
        return cleaned_data


class RechnungForm(forms.ModelForm):
    """Form for invoice management"""
    
    class Meta:
        model = Rechnung
        fields = ['faelligkeitsdatum', 'status', 'kommentar']
        widgets = {
            'faelligkeitsdatum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'kommentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default due date to 14 days from today if not set
        if not self.instance.pk and 'faelligkeitsdatum' not in self.initial:
            from django.utils import timezone
            self.initial['faelligkeitsdatum'] = timezone.now().date() + timedelta(days=14)
