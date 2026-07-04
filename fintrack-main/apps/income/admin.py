from django.contrib import admin
from .models import Income

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """
    Registers the Income model in Django admin.
    Exposes columns, filter sidebars, and source searching features.
    """
    list_display = ('title', 'user', 'amount', 'category', 'date', 'created_at')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    ordering = ('-date', '-created_at')
    date_hierarchy = 'date'
