from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Income
from .forms import IncomeForm

class IncomeListView(LoginRequiredMixin, ListView):
    """
    Renders list of user incomes (Earnings).
    Supports source/description text search, category filters, and pagination.
    """
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'incomes'
    paginate_by = 5

    def get_queryset(self):
        # Restrict queryset strictly to logged-in user
        queryset = Income.objects.filter(user=self.request.user)
        
        # Text query search (Source/Name or Description)
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
        context['categories'] = Income.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class IncomeCreateView(LoginRequiredMixin, CreateView):
    """
    Handles secure logging of a new Income record.
    Assigns the income owner to the current logged-in user automatically.
    """
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Income logged successfully!")
        return super().form_valid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    """
    Handles secure updates to an existing Income record.
    Filters query by owner to prevent ID tampering.
    """
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income_list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Income updated successfully!")
        return super().form_valid(form)


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles secure deletion of an Income record.
    Filters query by owner to prevent unauthorized requests.
    """
    model = Income
    template_name = 'income/income_confirm_delete.html'
    success_url = reverse_lazy('income_list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Income removed successfully!")
        return super().delete(request, *args, **kwargs)
