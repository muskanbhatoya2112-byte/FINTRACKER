from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Registers the Expense model in Django admin.
    Exposes columns, filter sidebars, and merchant searching features.
    """
    list_display = ('title', 'user', 'amount', 'category', 'date', 'created_at')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    ordering = ('-date', '-created_at')
    date_hierarchy = 'date'
