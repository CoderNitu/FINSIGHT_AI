from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from transactions.models import Transaction
from django.db.models import Sum
import json
from django.utils import timezone
from transactions.models import Budget
from transactions.forecaster import SpendingForecaster


class SignUpView(CreateView):
        """
        This view handles user registration using a built-in Django form.
        """
        form_class = UserCreationForm
        # reverse_lazy is used here because the URLs are not loaded when the file is imported.
        success_url = reverse_lazy('login')
        template_name = 'registration/signup.html'

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)

        # --- Chart Data ---
        spending_by_category = (
            Transaction.objects.filter(user=request.user, transaction_type='expense')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        chart_labels = [item['category__name'] if item['category__name'] else 'Uncategorized' for item in spending_by_category]
        chart_data = [float(item['total']) for item in spending_by_category]

        # --- Budget Data with Color Warning Logic ---
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        budgets = Budget.objects.filter(user=request.user, amount__gt=0).select_related('category')
        
        monthly_spending = (
            Transaction.objects.filter(user=request.user, transaction_type='expense', date__gte=start_of_month)
            .values('category__name')
            .annotate(total_spent=Sum('amount'))
        )
        spending_map = {item['category__name']: item['total_spent'] for item in monthly_spending}

        budget_progress = []
        for budget in budgets:
            spent = spending_map.get(budget.category.name, 0)
            percentage = (spent / budget.amount) * 100 if budget.amount > 0 else 0
            
            # THIS IS THE RESTORED LOGIC
            if percentage >= 100:
                bar_color_class = 'danger'
            elif percentage >= 75:
                bar_color_class = 'warning'
            else:
                bar_color_class = 'success'

            budget_progress.append({
                'category_name': budget.category.name,
                'budget_amount': budget.amount,
                'spent_amount': spent,
                'percentage': min(round(percentage, 2), 100),
                'bar_color_class': bar_color_class # The class is correctly passed
            })

        # --- Forecasting Data ---
        forecaster = SpendingForecaster(transactions)
        forecasted_spending = forecaster.forecast_next_30_days()

        # --- Final Context ---
        context = {
            'transactions': transactions,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
            'budget_progress': budget_progress,
            'forecasted_spending': forecasted_spending,
        }
        
        return render(request, 'core/dashboard.html', context)

