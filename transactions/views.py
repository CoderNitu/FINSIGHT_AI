from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
import json

from .forms import TransactionForm, CategoryForm
from .models import Transaction, Category, Keyword, Budget 
from .categorizer import TransactionCategorizer
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

import csv
from django.http import HttpResponse

# This view is for the modal form to add a category inline
class AddCategoryView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        form = CategoryForm(data)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            if Category.objects.filter(user=request.user, name__iexact=category_name).exists():
                return JsonResponse({'status': 'error', 'message': 'This category already exists.'}, status=400)
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return JsonResponse({'status': 'success', 'category_id': category.id, 'category_name': category.name})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data submitted.'}, status=400)

# This view handles adding a new transaction
class AddTransactionView(LoginRequiredMixin, View):
    def get(self, request):
        form = TransactionForm(user=request.user)
        return render(request, 'transactions/add_transaction.html', {'form': form})

    def post(self, request):
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
        return render(request, 'transactions/add_transaction.html', {'form': form})

# ===============================================================
# ===         THIS IS THE VIEW THAT WAS UPDATED             ===
# ===============================================================
class SuggestCategoryView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            description = data.get('description', '')
            if not description:
                return JsonResponse({'status': 'error', 'message': 'Description is empty.'}, status=400)

            # 1. Fetch the user's categories
            user_categories = Category.objects.filter(user=request.user)
            # 2. Fetch the user's custom keywords (the new line)
            user_keywords = Keyword.objects.filter(user=request.user)
            
            # 3. Initialize our smarter categorizer with both sets of data
            categorizer = TransactionCategorizer(user_categories, user_keywords)
            suggested_category_id = categorizer.suggest_category(description)

            if suggested_category_id:
                return JsonResponse({'status': 'success', 'category_id': suggested_category_id})
            else:
                return JsonResponse({'status': 'no_suggestion'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# This is the new view for the "Manage Smart Rules" page
class ManageRulesView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'transactions/manage_rules.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).prefetch_related('keywords')

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'add_keyword':
            category_id = request.POST.get('category_id')
            keyword_text = request.POST.get('keyword_text', '').strip().lower()
            if not keyword_text:
                return redirect(reverse('manage_rules'))
            category = get_object_or_404(Category, id=category_id, user=request.user)
            if not Keyword.objects.filter(user=request.user, text=keyword_text).exists():
                Keyword.objects.create(user=request.user, category=category, text=keyword_text)
        elif action == 'delete_keyword':
            keyword_id = request.POST.get('keyword_id')
            keyword = get_object_or_404(Keyword, id=keyword_id, user=request.user)
            keyword.delete()
        return redirect(reverse('manage_rules'))

class UpdateTransactionView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/edit_transaction.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        """Ensure users can only edit their own transactions."""
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        """Pass the current user to the form to filter categories."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        """Ensure users can only delete their own transactions."""
        return Transaction.objects.filter(user=self.request.user)

class ExportTransactionsCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 1. Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        # This header tells the browser to treat the response as a file attachment
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        # 2. Create a CSV writer object
        writer = csv.writer(response)

        # 3. Write the header row for the CSV file
        writer.writerow(['Date', 'Description', 'Category', 'Type', 'Amount'])

        # 4. Get all transactions for the current user, ordered by date
        transactions = Transaction.objects.filter(user=request.user).order_by('date')

        # 5. Loop through the transactions and write each one to a row in the CSV
        for transaction in transactions:
            writer.writerow([
                transaction.date.strftime('%Y-%m-%d'),
                transaction.description,
                transaction.category.name if transaction.category else 'N/A',
                transaction.transaction_type,
                transaction.amount
            ])

        # 6. Return the response to the user
        return response
    
class ManageBudgetsView(LoginRequiredMixin, View):
        template_name = 'transactions/manage_budgets.html'

        def get(self, request, *args, **kwargs):
            # Get all of the user's categories
            categories = Category.objects.filter(user=request.user)
            # Get all of the user's existing budgets
            budgets = Budget.objects.filter(user=request.user)
            
            # Create a dictionary to easily look up the budget amount for a category
            budget_map = {budget.category.id: budget.amount for budget in budgets}
            
            context = {
                'categories': categories,
                'budget_map': budget_map,
            }
            return render(request, self.template_name, context)

        def post(self, request, *args, **kwargs):
            # Loop through all the data sent from the form
            for key, value in request.POST.items():
                if key.startswith('budget_'):
                    category_id = key.split('_')[1]
                    try:
                        category = Category.objects.get(id=category_id, user=request.user)
                        amount = value if value else 0 # Default to 0 if empty
                        
                        # Update the budget if it exists, otherwise create a new one
                        Budget.objects.update_or_create(
                            user=request.user,
                            category=category,
                            defaults={'amount': amount}
                        )
                    except (Category.DoesNotExist, ValueError):
                        # Ignore if category doesn't exist or amount is invalid
                        continue
            return redirect('manage_budgets')