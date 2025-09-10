from django.urls import path
from .views import AddTransactionView, AddCategoryView, SuggestCategoryView, ManageRulesView, UpdateTransactionView, DeleteTransactionView, ExportTransactionsCSVView, ManageBudgetsView

urlpatterns = [
        path('add/', AddTransactionView.as_view(), name='add_transaction'),
        path('add_category/', AddCategoryView.as_view(), name='add_category'),
        path('suggest_category/', SuggestCategoryView.as_view(), name='suggest_category'),
        path('rules/', ManageRulesView.as_view(), name='manage_rules'),
        path('edit/<int:pk>/', UpdateTransactionView.as_view(), name='edit_transaction'),
        path('delete/<int:pk>/', DeleteTransactionView.as_view(), name='delete_transaction'),
        path('export/csv/', ExportTransactionsCSVView.as_view(), name='export_transactions_csv'),
        path('budgets/', ManageBudgetsView.as_view(), name='manage_budgets'),
    ]