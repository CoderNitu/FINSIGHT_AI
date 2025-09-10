from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'transaction_type', 'amount', 'category', 'description')
    list_filter = ('transaction_type', 'date', 'user')
    search_fields = ('description', 'user__username', 'category__name')
    
