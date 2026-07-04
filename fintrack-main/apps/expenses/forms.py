from django import forms
from .models import Expense
from django.core.exceptions import ValidationError
import datetime

class ExpenseForm(forms.ModelForm):
    """
    Expense creation/updating form.
    Binds fields with Bootstrap 5 input classes and runs custom validators.
    """
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description', 'receipt']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Apple Store',
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
                'placeholder': 'What was this for?',
                'class': 'form-control',
                'rows': 3,
                'id': 'id_description'
            }),
            'receipt': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'id_receipt',
                'accept': '.pdf, .jpg, .jpeg, .png'
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")
        return amount

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Merchant / name is required.")
        return title

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > datetime.date.today():
            raise ValidationError("Expense date cannot be in the future.")
        return date

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            # Enforce 10MB limit (10 * 1024 * 1024 bytes)
            if receipt.size > 10 * 1024 * 1024:
                raise ValidationError("Uploaded receipt cannot exceed 10MB in file size.")
        return receipt
