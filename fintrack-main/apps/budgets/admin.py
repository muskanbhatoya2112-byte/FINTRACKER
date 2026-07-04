from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Budget model.
    """
    list_display = ('user', 'category', 'limit', 'month', 'year', 'created_at')
    list_filter  = ('category', 'month', 'year')
    search_fields = ('user__username', 'user__email', 'category')
    ordering = ('-year', '-month', 'category')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Budget Details', {
            'fields': ('user', 'category', 'limit', 'month', 'year', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
