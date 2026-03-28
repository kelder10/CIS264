from django import forms
from .models import Review, ReviewImage


class ReviewForm(forms.ModelForm):
    """Form for submitting a review."""
    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Very Good'),
        (3, '3 - Good'),
        (2, '2 - Fair'),
        (1, '1 - Poor'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        initial=5
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Summarize your experience'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us about your experience...'
            }),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        return int(rating)


class ReviewImageForm(forms.ModelForm):
    """Form for adding images to reviews."""
    class Meta:
        model = ReviewImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional caption'
            }),
        }


ReviewImageFormSet = forms.inlineformset_factory(
    Review,
    ReviewImage,
    form=ReviewImageForm,
    extra=3,
    max_num=5,
    can_delete=False
)


class ReviewModerationForm(forms.ModelForm):
    """Form for moderating reviews (admin use)."""
    class Meta:
        model = Review
        fields = ['is_approved', 'is_featured', 'admin_response']
        widgets = {
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional response to the review...'
            }),
        }
