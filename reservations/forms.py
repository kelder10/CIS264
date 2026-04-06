from django import forms
from django.utils import timezone
from .models import Reservation, Waiver, PromoCode
from bikes.models import Bike, Accessory
from locations.models import Location
from datetime import timedelta 


class ReservationForm(forms.ModelForm):
    """Form for creating a reservation."""    
    pickup_location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True),
        empty_label="Select a Smart-Dock Location",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Pickup Dock Location"
    )

    rental_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat()
        })
    )

    end_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        label="Expected Return Time"
    )

    return_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat()
        })
    )

    accessories = forms.ModelMultipleChoiceField(
        queryset=Accessory.objects.filter(is_available=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Add Accessories (Optional)'
    )
    
    class Meta:
        model = Reservation
        fields = [
            'pickup_location', 
            'rental_date', 
            'end_time', 
            'return_date', 
            'rental_type', 
            'accessories', 
            'special_requests'
        ]
        widgets = {
            'rental_type': forms.Select(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests or requirements...'
            }),
        }
    
    def __init__(self, *args, bike=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.bike = bike
        if bike:
            self.fields['accessories'].queryset = Accessory.objects.filter(
                compatible_bikes__bike=bike,
                is_available=True
            )
    
    def clean(self):
        cleaned_data = super().clean()
        rental_date = cleaned_data.get('rental_date')
        return_date = cleaned_data.get('return_date')
        
        # Get the date from the server
        today = timezone.now().date()
        
        if rental_date and return_date:
            if rental_date < today - timedelta(days=1):
                raise forms.ValidationError('Rental date cannot be in the past.')
            
            if return_date < rental_date:
                raise forms.ValidationError('Return date must be after rental date.')
            
            if self.bike:
                if not self.bike.is_available_for_date(rental_date):
                    raise forms.ValidationError(f'Sorry, this bike is not available on {rental_date}.')
        
        return cleaned_data

class WaiverForm(forms.ModelForm):
    """Form for signing the rental waiver."""
    acknowledged_risks = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I acknowledge that bicycling involves inherent risks'
    )
    acknowledged_equipment = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to properly use and care for the rented equipment'
    )
    acknowledged_rules = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to follow all traffic laws and safety rules'
    )
    
    class Meta:
        model = Waiver
        fields = [
            'full_name', 'signature', 'acknowledged_risks',
            'acknowledged_equipment', 'acknowledged_rules',
            'emergency_contact_name', 'emergency_contact_phone'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full legal name'
            }),
            'signature': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type your name as digital signature'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact name'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact phone'
            }),
        }
    
    def clean_signature(self):
        signature = self.cleaned_data.get('signature')
        full_name = self.cleaned_data.get('full_name')
        
        if signature and full_name:
            # Signature should match full name (case insensitive)
            if signature.lower().strip() != full_name.lower().strip():
                raise forms.ValidationError(
                    'Your signature must match your full name exactly.'
                )
        
        return signature


class PromoCodeForm(forms.Form):
    """Form for applying a promo code."""
    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter promo code'
        })
    )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        
        try:
            promo = PromoCode.objects.get(code=code.upper(), is_active=True)
            if not promo.is_valid():
                raise forms.ValidationError('This promo code has expired or reached its usage limit.')
        except PromoCode.DoesNotExist:
            raise forms.ValidationError('Invalid promo code.')
        
        return code.upper()


class ReservationCancelForm(forms.Form):
    """Form for cancelling a reservation."""
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Reason for cancellation (optional)'
        })
    )
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I confirm that I want to cancel this reservation'
    )
