from django import forms
from .models import Income
from django.core.exceptions import ValidationError
import datetime

class IncomeForm(forms.ModelForm):
    """
    Income creation/updating form.
    Binds fields with Bootstrap 5 input classes and runs custom validators.
    """
    class Meta:
        model = Income
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Stripe Payout',
                'class': 'form-control',
                'id': 'id_title'
            }),
            'amount': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'class': 'form-control',
                'step': '0.01',
                'id': 'id_amount'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_category'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'id_date'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Earning details...',
                'class': 'form-control',
                'rows': 3,
                'id': 'id_description'
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Income amount must be greater than zero.")
        return amount

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Source / name is required.")
        return title

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > datetime.date.today():
            raise ValidationError("Income date cannot be in the future.")
        return date
