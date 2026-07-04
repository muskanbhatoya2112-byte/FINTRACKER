from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Expense
from .forms import ExpenseForm

class ExpenseListView(LoginRequiredMixin, ListView):
    """
    Renders list of user expenses.
    Supports merchant/description text search, category filters, and pagination.
    """
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 5

    def get_queryset(self):
        # Restrict queryset strictly to logged-in user
        queryset = Expense.objects.filter(user=self.request.user)
        
        # Text query search (Title/Merchant or Description)
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
            
        # Category selection filter
        category = self.request.GET.get('category', '').strip()
        if category and category != 'all':
            queryset = queryset.filter(category=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass variables to preserve search/filter state in HTML forms
        context['categories'] = Expense.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    """
    Handles secure creation of a new Expense record.
    Assigns the expense owner to the current logged-in user automatically.
    """
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Expense logged successfully!")
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    """
    Handles secure updates to an existing Expense record.
    Filters query by owner to prevent ID tampering.
    """
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Expense updated successfully!")
        return super().form_valid(form)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles secure deletion of an Expense record.
    Filters query by owner to prevent unauthorized requests.
    """
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Expense removed successfully!")
        return super().delete(request, *args, **kwargs)
