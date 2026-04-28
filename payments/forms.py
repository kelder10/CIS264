from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    """Form for processing payments."""
    # Card details (for demo, these are not actually processed)
    card_number = forms.CharField(
        max_length=19,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'autocomplete': 'cc-number'
        })
    )
    card_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name on card',
            'autocomplete': 'cc-name'
        })
    )
    expiry_month = forms.ChoiceField(
        choices=[(f'{i:02d}', f'{i:02d}') for i in range(1, 13)],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    expiry_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(2024, 2035)],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cvv = forms.CharField(
        max_length=4,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'autocomplete': 'cc-csc'
        })
    )
    promo_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter promo code (optional)'
        })
    )
    save_card = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Save this card for future payments'
    )
    
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.RadioSelect(choices=Payment.PAYMENT_METHODS),
        }
    
    def __init__(self, *args, reservation=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reservation = reservation
        # Set default payment method
        self.fields['payment_method'].initial = 'credit_card'
    
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number', '').replace(' ', '').replace('-', '')
        
        # Basic validation for demo
        if not card_number.isdigit():
            raise forms.ValidationError('Card number must contain only digits.')
        
        if len(card_number) < 13 or len(card_number) > 19:
            raise forms.ValidationError('Card number must be between 13 and 19 digits.')
        
        # Luhn algorithm check (basic)
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            total = sum(odd_digits)
            for d in even_digits:
                d *= 2
                if d > 9:
                    d -= 9
                total += d
            return total % 10 == 0
        
        if not luhn_check(card_number):
            raise forms.ValidationError('Invalid card number. Please check and try again.')
        
        return card_number
    
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv', '')
        
        if not cvv.isdigit():
            raise forms.ValidationError('CVV must contain only digits.')
        
        if len(cvv) < 3 or len(cvv) > 4:
            raise forms.ValidationError('CVV must be 3 or 4 digits.')
        
        return cvv
    
    def clean_promo_code(self):
        code = self.cleaned_data.get('promo_code', '').upper()
        
        if code:
            from reservations.models import PromoCode
            try:
                promo = PromoCode.objects.get(code=code, is_active=True)
                if not promo.is_valid():
                    raise forms.ValidationError('This promo code has expired or reached its usage limit.')
                if self.reservation and self.reservation.subtotal < promo.minimum_order:
                    raise forms.ValidationError(f'Minimum order of ${promo.minimum_order} required.')
                if self.reservation:
                    business_rule_error = promo.get_business_rule_error(self.reservation)
                    if business_rule_error:
                        raise forms.ValidationError(business_rule_error)
            except PromoCode.DoesNotExist:
                raise forms.ValidationError('Invalid promo code.')
        
        return code
    
    def get_card_brand(self, card_number):
        """Determine card brand from number."""
        if card_number.startswith('4'):
            return 'Visa'
        elif card_number.startswith(('51', '52', '53', '54', '55')):
            return 'Mastercard'
        elif card_number.startswith(('34', '37')):
            return 'American Express'
        elif card_number.startswith('6'):
            return 'Discover'
        return 'Unknown'


class SimulatedPaymentForm(forms.Form):
    """Simplified form for simulated payment (no real card validation)."""
    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHODS,
        widget=forms.RadioSelect,
        initial='credit_card'
    )
    promo_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter promo code (optional)'
        })
    )

    def __init__(self, *args, reservation=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reservation = reservation
    
    def clean_promo_code(self):
        code = self.cleaned_data.get('promo_code', '').upper()
        
        if code:
            from reservations.models import PromoCode
            try:
                promo = PromoCode.objects.get(code=code, is_active=True)
                if not promo.is_valid():
                    raise forms.ValidationError('This promo code has expired or reached its usage limit.')
                if self.reservation and self.reservation.subtotal < promo.minimum_order:
                    raise forms.ValidationError(f'Minimum order of ${promo.minimum_order} required.')
                if self.reservation:
                    business_rule_error = promo.get_business_rule_error(self.reservation)
                    if business_rule_error:
                        raise forms.ValidationError(business_rule_error)
            except PromoCode.DoesNotExist:
                raise forms.ValidationError('Invalid promo code.')
        
        return code
