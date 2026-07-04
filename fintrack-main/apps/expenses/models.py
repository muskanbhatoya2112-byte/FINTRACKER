from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Expense(models.Model):
    """
    Expense database model configured for MySQL backend storage.
    Tracks users' individual transactions, categories, and uploaded file receipts.
    """
    CATEGORY_CHOICES = [
        ('housing', 'Housing'),
        ('food_groceries', 'Food & Groceries'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('shopping', 'Shopping'),
        ('technology', 'Technology'),
        ('dining', 'Dining'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    title = models.CharField(max_length=255, verbose_name="Merchant / Name")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    receipt = models.FileField(
        upload_to='receipts/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.get_category_display()})"
