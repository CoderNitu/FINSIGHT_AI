# We need to import the built-in User model to link transactions to users
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Represents a category for a transaction, e.g., 'Food', 'Transport', 'Salary'.
    Each category is specific to a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        # This is how the object will be displayed in the Django admin
        return self.name
    
    class Meta:
        # This ensures that a user cannot have two categories with the same name
        unique_together = ('user', 'name')
        verbose_name_plural = "Categories"


class Transaction(models.Model):
    """
    Represents a single financial transaction (either an income or an expense).
    """
    TRANSACTION_TYPE_CHOICES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.description} ({self.amount})"

    class Meta:
        # Orders transactions by date, with the most recent ones first
        ordering = ['-date']

class Keyword(models.Model):
        """
        Represents a user-defined keyword that maps to one of their categories.
        """
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='keywords')
        category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='keywords')
        text = models.CharField(max_length=100)
    
        def __str__(self):
            return f"'{self.text}' -> {self.category.name} (for {self.user.username})"
    
        class Meta:
            # A user cannot have the same keyword text twice
            unique_together = ('user', 'text')

class Budget(models.Model):
        """
        Represents a user's monthly budget for a specific category.
        """
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
        category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        # We can add month/year fields later, for now, it's a general monthly budget.
    
        def __str__(self):
            return f"{self.user.username}'s budget for {self.category.name}: ₹{self.amount}"
    
        class Meta:
            # A user can only have one budget per category
            unique_together = ('user', 'category') 