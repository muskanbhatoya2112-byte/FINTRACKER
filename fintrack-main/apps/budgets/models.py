from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
import datetime


class Budget(models.Model):
    """
    Budget model for FinTrack.
    Tracks a user's spending limit for a specific category within a given month/year.
    Links to the Expense model via category matching to compute real-time spending progress.
    Stored in MySQL via Django ORM.
    """

    # Budget category choices — aligned with Expense.CATEGORY_CHOICES for accurate spend tracking
    CATEGORY_CHOICES = [
        ('housing',        'Housing'),
        ('food_groceries', 'Food & Groceries'),
        ('entertainment',  'Entertainment'),
        ('utilities',      'Utilities'),
        ('shopping',       'Shopping'),
        ('technology',     'Technology'),
        ('dining',         'Dining'),
        ('other',          'Other'),
    ]

    # Month choices (1–12) displayed as full month names
    MONTH_CHOICES = [
        (1,  'January'),
        (2,  'February'),
        (3,  'March'),
        (4,  'April'),
        (5,  'May'),
        (6,  'June'),
        (7,  'July'),
        (8,  'August'),
        (9,  'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name='Category'
    )
    limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Budget Limit ($)'
    )
    month = models.PositiveSmallIntegerField(
        choices=MONTH_CHOICES,
        verbose_name='Month'
    )
    year = models.PositiveIntegerField(verbose_name='Year')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-month', 'category']
        # Prevent duplicate budget entries for same user/category/month/year
        unique_together = [('user', 'category', 'month', 'year')]
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return f"{self.get_category_display()} Budget — {self.get_month_display()} {self.year} (${self.limit})"

    # ── Computed Properties ─────────────────────────────────────────────────

    @property
    def spent(self):
        """
        Sum of all Expense amounts for this user/category/month/year.
        Imports Expense inline to avoid circular imports.
        """
        from expenses.models import Expense
        from django.db.models import Sum
        result = Expense.objects.filter(
            user=self.user,
            category=self.category,
            date__month=self.month,
            date__year=self.year,
        ).aggregate(total=Sum('amount'))['total']
        return result or Decimal('0.00')

    @property
    def remaining(self):
        """Remaining budget = limit − spent. Can be negative (overspent)."""
        return self.limit - self.spent

    @property
    def percent_used(self):
        """Percentage of the budget consumed (0–100+). Returns 0 if limit is 0."""
        if self.limit == 0:
            return 0
        pct = (self.spent / self.limit) * 100
        return round(float(pct), 1)

    @property
    def is_overspent(self):
        """True when actual spending has exceeded the budget limit."""
        return self.spent > self.limit

    @property
    def is_warning(self):
        """True when spending has reached or exceeded 80 % of the limit."""
        return self.percent_used >= 80 and not self.is_overspent

    @property
    def status_label(self):
        """Human-readable status string for template display."""
        if self.is_overspent:
            return 'Overspent'
        if self.is_warning:
            return 'Warning'
        return 'On Track'

    @property
    def status_color(self):
        """Bootstrap/CSS color keyword matching the current status."""
        if self.is_overspent:
            return 'danger'
        if self.is_warning:
            return 'warning'
        return 'success'
