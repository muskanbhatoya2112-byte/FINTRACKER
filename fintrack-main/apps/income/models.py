from django.db import models
from django.conf import settings

class Income(models.Model):
    """
    Income database model configured for MySQL backend storage.
    Tracks users' individual earnings, sources, categories, and dates.
    """
    CATEGORY_CHOICES = [
        ('salary', 'Salary / Direct Deposit'),
        ('freelance', 'Freelance / Contract'),
        ('investments', 'Investments / Dividends'),
        ('business', 'Business / Revenue'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='incomes'
    )
    title = models.CharField(max_length=255, verbose_name="Source / Name")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.get_category_display()})"
