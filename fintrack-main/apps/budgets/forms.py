from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
import datetime
from .models import Budget


class BudgetForm(forms.ModelForm):
    """
    Budget creation / update form.
    Renders Bootstrap 5 widgets and validates limit, month, and year.
    """

    class Meta:
        model = Budget
        fields = ['category', 'limit', 'month', 'year', 'notes']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_category',
            }),
            'limit': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'id': 'id_limit',
            }),
            'month': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_month',
            }),
            'year': forms.NumberInput(attrs={
                'placeholder': str(datetime.date.today().year),
                'class': 'form-control',
                'min': '2000',
                'max': '2100',
                'id': 'id_year',
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Optional notes about this budget...',
                'class': 'form-control',
                'rows': 3,
                'id': 'id_notes',
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        # Default month/year to current period for new budgets
        today = datetime.date.today()
        if not self.instance.pk:
            self.fields['month'].initial = today.month
            self.fields['year'].initial = today.year

    def clean_limit(self):
        limit = self.cleaned_data.get('limit')
        if limit is not None and limit <= Decimal('0'):
            raise ValidationError("Budget limit must be greater than zero.")
        return limit

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is not None:
            if year < 2000 or year > 2100:
                raise ValidationError("Please enter a valid year between 2000 and 2100.")
        return year

    def clean_month(self):
        month = self.cleaned_data.get('month')
        if month is not None and not (1 <= month <= 12):
            raise ValidationError("Please select a valid month.")
        return month

    def clean(self):
        cleaned_data = super().clean()
        user = self.user or getattr(self.instance, 'user', None)
        category = cleaned_data.get('category')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        if user and category and month and year:
            duplicate = Budget.objects.filter(
                user=user,
                category=category,
                month=month,
                year=year,
            ).exclude(pk=self.instance.pk).exists()
            if duplicate:
                raise ValidationError(
                    "A budget for this category and month already exists. Edit the existing one instead."
                )
        return cleaned_data
