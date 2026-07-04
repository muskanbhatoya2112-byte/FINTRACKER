from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse
from decimal import Decimal
import datetime
import json

from income.models import Income
from expenses.models import Expense
from budgets.models import Budget


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Class-based view for the central financial dashboard.
    Protected by LoginRequiredMixin, redirecting anonymous users to the login route.
    """
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = datetime.date.today()

        total_income = (
            Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )
        total_expenses = (
            Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )
        current_balance = total_income - total_expenses

        monthly_income = (
            Income.objects.filter(
                user=user, date__year=today.year, date__month=today.month
            ).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )
        monthly_expense = (
            Expense.objects.filter(
                user=user, date__year=today.year, date__month=today.month
            ).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )

        if today.month == 1:
            prev_month, prev_year = 12, today.year - 1
        else:
            prev_month, prev_year = today.month - 1, today.year

        prev_income = (
            Income.objects.filter(
                user=user, date__year=prev_year, date__month=prev_month
            ).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )
        prev_expense = (
            Expense.objects.filter(
                user=user, date__year=prev_year, date__month=prev_month
            ).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )
        prev_net = prev_income - prev_expense
        current_net = monthly_income - monthly_expense

        if prev_net != 0:
            change_pct = ((current_net - prev_net) / abs(prev_net)) * 100
            balance_change = f"{'+' if change_pct >= 0 else ''}{change_pct:.1f}%"
        elif current_net != 0:
            balance_change = '+100%'
        else:
            balance_change = '0%'

        if prev_income > 0:
            income_diff = ((monthly_income - prev_income) / prev_income) * 100
            income_status = (
                f"Up {income_diff:.0f}% vs last month"
                if income_diff >= 0
                else f"Down {abs(income_diff):.0f}% vs last month"
            )
        elif monthly_income > 0:
            income_status = 'Income logged this month'
        else:
            income_status = 'No income logged yet'

        budgets = Budget.objects.filter(
            user=user, month=today.month, year=today.year
        )
        total_budget_limit = sum(b.limit for b in budgets) or Decimal('0.00')
        if total_budget_limit > 0:
            budget_pct = float(monthly_expense / total_budget_limit * 100)
            if budget_pct > 100:
                expense_status = f"{budget_pct - 100:.0f}% over budget"
            elif budget_pct >= 80:
                expense_status = f"{budget_pct:.0f}% of budget used"
            else:
                expense_status = f"Within budget ({budget_pct:.0f}%)"
        else:
            expense_status = 'No budgets set for this month'

        if monthly_income > 0:
            savings_goal_percent = min(
                100,
                max(0, round(float((monthly_income - monthly_expense) / monthly_income * 100))),
            )
        else:
            savings_goal_percent = 0

        context['metrics'] = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_balance': current_balance,
            'balance_change': balance_change,
            'monthly_income': monthly_income,
            'income_status': income_status,
            'monthly_expense': monthly_expense,
            'expense_status': expense_status,
            'savings_goal_percent': savings_goal_percent,
        }

        transactions = []
        for income in Income.objects.filter(user=user).order_by('-date', '-created_at')[:10]:
            transactions.append({
                'name': income.title,
                'category': income.get_category_display(),
                'category_key': income.category,
                'date': income.date.strftime('%b %d, %Y'),
                'date_sort': income.date,
                'created_at': income.created_at,
                'status': 'COMPLETED',
                'amount': income.amount,
                'is_income': True,
            })
        for expense in Expense.objects.filter(user=user).order_by('-date', '-created_at')[:10]:
            transactions.append({
                'name': expense.title,
                'category': expense.get_category_display(),
                'category_key': expense.category,
                'date': expense.date.strftime('%b %d, %Y'),
                'date_sort': expense.date,
                'created_at': expense.created_at,
                'status': 'COMPLETED',
                'amount': expense.amount,
                'is_income': False,
            })
        transactions.sort(key=lambda tx: (tx['date_sort'], tx['created_at']), reverse=True)
        context['recent_transactions'] = transactions[:5]

        context['budget_status'] = [
            {
                'category': budget.get_category_display(),
                'category_key': budget.category,
                'limit': budget.limit,
                'spent': budget.spent,
                'remaining': budget.remaining,
                'percent_used': budget.percent_used,
                'status_label': budget.status_label,
                'status_color': budget.status_color,
            }
            for budget in budgets
        ]

        category_labels = dict(Expense.CATEGORY_CHOICES)
        top_categories = (
            Expense.objects.filter(
                user=user, date__year=today.year, date__month=today.month
            )
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:5]
        )
        context['top_spending_categories'] = [
            {
                'category': category_labels.get(row['category'], row['category']),
                'category_key': row['category'],
                'amount': row['total'] or Decimal('0.00'),
            }
            for row in top_categories
        ]

        spending_labels = []
        spending_data = []
        for months_back in range(9, -1, -1):
            month = today.month - months_back
            year = today.year
            while month <= 0:
                month += 12
                year -= 1
            month_total = (
                Expense.objects.filter(
                    user=user, date__year=year, date__month=month
                ).aggregate(total=Sum('amount'))['total']
                or Decimal('0.00')
            )
            spending_labels.append(datetime.date(year, month, 1).strftime('%b'))
            spending_data.append(float(month_total))

        context['spending_chart'] = {
            'labels': json.dumps(spending_labels),
            'data': json.dumps(spending_data),
        }

        if budgets:
            on_track = sum(1 for b in budgets if not b.is_overspent and not b.is_warning)
            at_risk = len(budgets) - on_track
            on_track_pct = round(on_track / len(budgets) * 100)
            at_risk_pct = round(at_risk / len(budgets) * 100)
            stability_score = max(
                0,
                100 - round(
                    sum(1 for b in budgets if b.is_overspent) / len(budgets) * 50
                    + sum(1 for b in budgets if b.is_warning) / len(budgets) * 20
                ),
            )
        else:
            on_track_pct = 100
            at_risk_pct = 0
            stability_score = 100 if monthly_expense == 0 else 50

        context['budget_chart'] = {
            'labels': json.dumps(['On Track', 'At Risk']),
            'data': json.dumps([on_track_pct, at_risk_pct]),
            'stability_score': stability_score,
        }
        context['budget_list_url'] = (
            f"{reverse('budget_list')}?month={today.month}&year={today.year}"
        )

        return context
