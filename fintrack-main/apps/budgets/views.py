from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from decimal import Decimal
import datetime

from .models import Budget
from .forms import BudgetForm


class BudgetListView(LoginRequiredMixin, ListView):
    """
    Main budgets dashboard view.
    Renders all budgets for the selected month/year with real-time progress.
    Defaults to the current calendar month. Supports month/year filter via GET params.
    """
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        today = datetime.date.today()
        self.selected_month = int(self.request.GET.get('month', today.month))
        self.selected_year  = int(self.request.GET.get('year',  today.year))
        return Budget.objects.filter(
            user=self.request.user,
            month=self.selected_month,
            year=self.selected_year,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budgets = context['budgets']

        # ── Summary metrics ────────────────────────────────────────────────
        total_limit   = sum(b.limit   for b in budgets) or Decimal('0.00')
        total_spent   = sum(b.spent   for b in budgets) or Decimal('0.00')
        total_remaining = total_limit - total_spent

        overspent_count = sum(1 for b in budgets if b.is_overspent)
        warning_count   = sum(1 for b in budgets if b.is_warning)

        # ── Month navigation helpers ───────────────────────────────────────
        context.update({
            'selected_month': self.selected_month,
            'selected_year':  self.selected_year,
            'month_name': datetime.date(self.selected_year, self.selected_month, 1).strftime('%B'),
            'total_limit':     total_limit,
            'total_spent':     total_spent,
            'total_remaining': total_remaining,
            'overall_percent': round(float(total_spent / total_limit * 100), 1) if total_limit else 0,
            'overspent_count': overspent_count,
            'warning_count':   warning_count,
            'months':          Budget.MONTH_CHOICES,
            'year_range':      range(datetime.date.today().year - 3, datetime.date.today().year + 2),
        })
        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new budget entry. Validates uniqueness (category + month + year per user)
    and auto-assigns the logged-in user as owner.
    """
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Budget created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('budget_list')}?month={self.object.month}&year={self.object.year}"


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing budget. Scoped to the owning user to prevent ID tampering.
    """
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Budget updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('budget_list')}?month={self.object.month}&year={self.object.year}"


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a budget entry. Scoped to the owning user.
    Redirects back to the same month/year context after deletion.
    """
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_success_url(self):
        return f"{reverse('budget_list')}?month={self.object.month}&year={self.object.year}"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Budget removed successfully!")
        return super().delete(request, *args, **kwargs)
